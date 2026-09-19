"""Workflow scanner service — operational AI Co-Pilot.

Scans AEs, Visits, and Milestones for bottlenecks, overdue items, and
deadline risks. Sends a plain-data summary to Claude and saves the
resulting operational alerts to the workflow_alerts table.

No clinical or medical judgments are made here or by Claude.
"""
import json
import logging
from datetime import date, timedelta

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pharmacovigilance import AdverseEvent
from app.models.visit import ParticipantVisit
from app.models.trial import TrialMilestone
from app.models.workflow_alert import WorkflowAlert
from app.services.ai_service import ask_claude

logger = logging.getLogger(__name__)

# Thresholds
_AE_REVIEW_WINDOW_DAYS = 5      # AEs pending review beyond this are flagged
_VISIT_OVERDUE_DAYS = 0         # Visits past scheduled_date are overdue
_MILESTONE_WARNING_DAYS = 7     # Milestones due within this window are flagged

_WORKFLOW_SYSTEM_PROMPT = (
    "You are an operational workflow assistant for a clinical trial management system (CTMS). "
    "You do NOT make clinical or medical judgments of any kind. "
    "Your sole job is to identify process bottlenecks, missed deadlines, and workflow delays "
    "from the operational data provided, and write clear, concise, plain-language alert messages "
    "for the trial coordinator.\n\n"
    "Respond ONLY with a valid JSON array — no markdown, no extra text — where each element has:\n"
    '{"entity_type": "AE"|"Visit"|"Milestone", '
    '"entity_id": "<uuid>", '
    '"alert_type": "bottleneck"|"deadline_risk"|"delay", '
    '"message": "<plain-language operational message>", '
    '"severity": "low"|"medium"|"high"}\n\n'
    "Guidelines:\n"
    "- high: items severely overdue or blocking regulatory deadlines\n"
    "- medium: items approaching deadlines or moderately delayed\n"
    "- low: items worth watching but not yet critical\n"
    "- Message examples: 'AE #204 has been pending review for 6 days — exceeds the 5-day internal review window.' "
    "or 'Visit for Participant #58 was scheduled 3 days ago and is still marked SCHEDULED.'\n"
    "- Do not mention medical terms, symptoms, diagnoses, or clinical outcomes."
)


async def scan_and_generate_alerts(db: AsyncSession) -> list[dict]:
    """Scan workflow health and generate AI-powered operational alerts.

    Clears previous alerts, scans AEs/Visits/Milestones, sends a summary
    to Claude, and writes the results to workflow_alerts.

    Returns the list of alert dicts that were saved.
    """
    today = date.today()
    flagged_items: list[dict] = []

    # --- Scan AEs pending review past threshold ---
    ae_cutoff = today - timedelta(days=_AE_REVIEW_WINDOW_DAYS)
    ae_result = await db.execute(
        select(AdverseEvent).where(
            AdverseEvent.is_deleted == False,
            AdverseEvent.status == "REPORTED",
            AdverseEvent.reported_date != None,
            AdverseEvent.reported_date <= ae_cutoff,
        )
    )
    for ae in ae_result.scalars().all():
        days_pending = (today - ae.reported_date).days
        flagged_items.append({
            "entity_type": "AE",
            "entity_id": str(ae.id),
            "label": ae.event_term or "Adverse Event",
            "participant_id": str(ae.participant_id),
            "days_pending": days_pending,
            "status": ae.status,
        })

    # --- Scan Visits that are overdue ---
    visit_result = await db.execute(
        select(ParticipantVisit).where(
            ParticipantVisit.status.in_(["SCHEDULED", "OVERDUE"]),
            ParticipantVisit.scheduled_date != None,
            ParticipantVisit.scheduled_date < today,
        )
    )
    for visit in visit_result.scalars().all():
        days_overdue = (today - visit.scheduled_date).days
        flagged_items.append({
            "entity_type": "Visit",
            "entity_id": str(visit.id),
            "label": visit.visit_name or "Visit",
            "participant_id": str(visit.participant_id),
            "days_overdue": days_overdue,
            "scheduled_date": str(visit.scheduled_date),
            "status": visit.status,
        })

    # --- Scan Milestones approaching or past due ---
    milestone_cutoff = today + timedelta(days=_MILESTONE_WARNING_DAYS)
    milestone_result = await db.execute(
        select(TrialMilestone).where(
            TrialMilestone.status == "PENDING",
            TrialMilestone.planned_date != None,
            TrialMilestone.planned_date <= milestone_cutoff,
        )
    )
    for ms in milestone_result.scalars().all():
        days_until = (ms.planned_date - today).days  # negative = overdue
        flagged_items.append({
            "entity_type": "Milestone",
            "entity_id": str(ms.id),
            "label": ms.name,
            "trial_id": str(ms.trial_id),
            "planned_date": str(ms.planned_date),
            "days_until_due": days_until,
            "status": ms.status,
        })

    if not flagged_items:
        logger.info("Workflow scan: no flagged items found — clearing old alerts")
        await db.execute(delete(WorkflowAlert))
        await db.commit()
        return []

    # Build the summary prompt for Claude
    summary_lines = [f"Today's date: {today}", f"Flagged items ({len(flagged_items)}):"]
    for i, item in enumerate(flagged_items, 1):
        summary_lines.append(f"  {i}. {json.dumps(item)}")
    prompt = (
        "The following items have been flagged by the CTMS workflow scanner. "
        "Identify which represent real operational concerns and write plain-language alert messages.\n\n"
        + "\n".join(summary_lines)
    )

    # Call Claude with fallback for offline / demo mode
    raw = ""
    alerts_data: list[dict] = []
    try:
        raw = await ask_claude(prompt, system_prompt=_WORKFLOW_SYSTEM_PROMPT)
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        alerts_data = json.loads(cleaned)
    except Exception as exc:
        logger.warning("Workflow scanner: AI service unavailable (%s) — using operational rule engine for demo alerts", exc)
        # Operational rule-based fallback for demo environments without active API key
        for item in flagged_items:
            etype = item.get("entity_type")
            eid = item.get("entity_id")
            if etype == "AE":
                days = item.get("days_pending", 0)
                sev = "high" if days >= 8 else "medium"
                alerts_data.append({
                    "entity_type": "AE",
                    "entity_id": eid,
                    "alert_type": "bottleneck",
                    "message": f"AE '{item.get('label')}' (Participant {item.get('participant_id')[:8]}) pending review for {days} days — exceeds internal 5-day review window.",
                    "severity": sev,
                })
            elif etype == "Visit":
                days = item.get("days_overdue", 0)
                sev = "high" if days >= 5 else "medium" if days >= 3 else "low"
                alerts_data.append({
                    "entity_type": "Visit",
                    "entity_id": eid,
                    "alert_type": "delay",
                    "message": f"{item.get('label')} for Participant {item.get('participant_id')[:8]} is {days} day(s) overdue (scheduled {item.get('scheduled_date')}).",
                    "severity": sev,
                })
            elif etype == "Milestone":
                days_left = item.get("days_until_due", 0)
                if days_left < 0:
                    alerts_data.append({
                        "entity_type": "Milestone",
                        "entity_id": eid,
                        "alert_type": "deadline_risk",
                        "message": f"Trial milestone '{item.get('label')}' is {abs(days_left)} day(s) past due target date ({item.get('planned_date')}).",
                        "severity": "high",
                    })
                else:
                    alerts_data.append({
                        "entity_type": "Milestone",
                        "entity_id": eid,
                        "alert_type": "deadline_risk",
                        "message": f"Trial milestone '{item.get('label')}' due in {days_left} day(s) ({item.get('planned_date')}) — action required.",
                        "severity": "medium" if days_left <= 3 else "low",
                    })

    # Validate and normalise
    valid_entity_types = {"AE", "Visit", "Milestone"}
    valid_alert_types = {"bottleneck", "deadline_risk", "delay"}
    valid_severities = {"low", "medium", "high"}
    clean_alerts: list[dict] = []
    for item in alerts_data:
        if (
            item.get("entity_type") in valid_entity_types
            and item.get("alert_type") in valid_alert_types
            and item.get("severity") in valid_severities
            and item.get("message")
            and item.get("entity_id")
        ):
            clean_alerts.append(item)
        else:
            logger.warning("Workflow scanner: invalid alert item skipped: %r", item)

    # Persist — clear old alerts, insert new ones
    await db.execute(delete(WorkflowAlert))
    for alert in clean_alerts:
        db.add(WorkflowAlert(
            entity_type=alert["entity_type"],
            entity_id=alert["entity_id"],
            alert_type=alert["alert_type"],
            message=alert["message"],
            severity=alert["severity"],
        ))
    await db.commit()
    logger.info("Workflow scan complete: %d alerts saved", len(clean_alerts))
    return clean_alerts
