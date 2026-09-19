"""Workflow Alerts API — AI Co-Pilot endpoints.

POST /workflow-alerts/scan  — trigger a workflow health scan
GET  /workflow-alerts        — retrieve current alerts, sorted by severity
"""
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, case
from typing import List
from datetime import datetime
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.workflow_alert import WorkflowAlert
from app.services.workflow_scanner import scan_and_generate_alerts

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/workflow-alerts", tags=["Workflow Alerts"])


class WorkflowAlertOut(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    alert_type: str
    message: str
    severity: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


@router.post("/scan")
async def trigger_scan(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR")),
):
    """Trigger a workflow health scan and regenerate alerts."""
    alerts = await scan_and_generate_alerts(db)
    return {"message": f"Scan complete. {len(alerts)} alert(s) generated.", "count": len(alerts)}


@router.get("", response_model=List[WorkflowAlertOut])
async def list_alerts(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Return all current workflow alerts sorted by severity (high first)."""
    severity_order = case(
        (WorkflowAlert.severity == "high", 1),
        (WorkflowAlert.severity == "medium", 2),
        (WorkflowAlert.severity == "low", 3),
        else_=4,
    )
    result = await db.execute(
        select(WorkflowAlert)
        .where(WorkflowAlert.is_deleted == False)
        .order_by(severity_order, WorkflowAlert.created_at.desc())
    )
    return result.scalars().all()
