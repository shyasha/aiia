from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.trial import Trial, StudyArm, Intervention, TrialMilestone
from app.models.participant import Participant
from app.models.site import SiteAssignment
from app.schemas.trial import TrialCreate, TrialUpdate, TrialOut, StudyArmCreate, InterventionCreate, MilestoneCreate, StudyArmOut, InterventionOut
from typing import List, Optional

router = APIRouter(prefix="/trials", tags=["Trials"])

@router.get("/", response_model=List[TrialOut])
async def list_trials(skip: int = 0, limit: int = 50, status: Optional[str] = None, phase: Optional[str] = None, search: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(Trial).where(Trial.is_deleted == False)
    if status:
        query = query.where(Trial.status == status)
    if phase:
        query = query.where(Trial.phase == phase)
    if search:
        query = query.where(Trial.title.ilike(f"%{search}%"))
    query = query.order_by(Trial.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    trials = result.scalars().all()
    out = []
    for t in trials:
        pc = await db.execute(select(func.count()).select_from(Participant).where(Participant.trial_id == t.id, Participant.is_deleted == False))
        sc = await db.execute(select(func.count()).select_from(SiteAssignment).where(SiteAssignment.trial_id == t.id))
        out.append(TrialOut(
            id=t.id, title=t.title, short_title=t.short_title, protocol_number=t.protocol_number,
            registration_number=t.registration_number, phase=t.phase, study_type=t.study_type,
            intervention_type=t.intervention_type, therapeutic_area=t.therapeutic_area,
            ayurveda_system=t.ayurveda_system, primary_objective=t.primary_objective,
            planned_sample_size=t.planned_sample_size, sponsor=t.sponsor,
            start_date=t.start_date, expected_end_date=t.expected_end_date,
            actual_end_date=t.actual_end_date, status=t.status, description=t.description,
            created_at=t.created_at, participant_count=pc.scalar() or 0, site_count=sc.scalar() or 0
        ))
    return out

@router.post("/", response_model=TrialOut)
async def create_trial(data: TrialCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "PRINCIPAL_INVESTIGATOR"))):
    trial = Trial(**data.model_dump())
    db.add(trial)
    await db.commit()
    await db.refresh(trial)
    return TrialOut(id=trial.id, title=trial.title, short_title=trial.short_title, protocol_number=trial.protocol_number, phase=trial.phase, status=trial.status, created_at=trial.created_at, study_type=trial.study_type, therapeutic_area=trial.therapeutic_area, start_date=trial.start_date, expected_end_date=trial.expected_end_date, planned_sample_size=trial.planned_sample_size, sponsor=trial.sponsor, description=trial.description)

@router.get("/{trial_id}", response_model=TrialOut)
async def get_trial(trial_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Trial).where(Trial.id == trial_id))
    trial = result.scalar_one_or_none()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    pc = await db.execute(select(func.count()).select_from(Participant).where(Participant.trial_id == trial.id))
    sc = await db.execute(select(func.count()).select_from(SiteAssignment).where(SiteAssignment.trial_id == trial.id))
    return TrialOut(
        id=trial.id, title=trial.title, short_title=trial.short_title, protocol_number=trial.protocol_number,
        registration_number=trial.registration_number, phase=trial.phase, study_type=trial.study_type,
        intervention_type=trial.intervention_type, therapeutic_area=trial.therapeutic_area,
        ayurveda_system=trial.ayurveda_system, primary_objective=trial.primary_objective,
        planned_sample_size=trial.planned_sample_size, sponsor=trial.sponsor,
        start_date=trial.start_date, expected_end_date=trial.expected_end_date, status=trial.status,
        description=trial.description, created_at=trial.created_at, participant_count=pc.scalar() or 0, site_count=sc.scalar() or 0
    )

@router.put("/{trial_id}", response_model=TrialOut)
async def update_trial(trial_id: str, data: TrialUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "PRINCIPAL_INVESTIGATOR"))):
    result = await db.execute(select(Trial).where(Trial.id == trial_id))
    trial = result.scalar_one_or_none()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(trial, key, value)
    await db.commit()
    return TrialOut(id=trial.id, title=trial.title, short_title=trial.short_title, protocol_number=trial.protocol_number, phase=trial.phase, status=trial.status, created_at=trial.created_at)

@router.get("/{trial_id}/arms", response_model=List[StudyArmOut])
async def get_trial_arms(trial_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(StudyArm).where(StudyArm.trial_id == trial_id))
    return result.scalars().all()

@router.post("/{trial_id}/arms", response_model=StudyArmOut)
async def create_study_arm(trial_id: str, data: StudyArmCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    arm = StudyArm(trial_id=trial_id, **data.model_dump())
    db.add(arm)
    await db.commit()
    await db.refresh(arm)
    return arm

@router.get("/{trial_id}/interventions", response_model=List[InterventionOut])
async def get_trial_interventions(trial_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    """Return all interventions for a trial — used to populate the causative drug dropdown on AE forms."""
    result = await db.execute(select(Intervention).where(Intervention.trial_id == trial_id))
    return result.scalars().all()
