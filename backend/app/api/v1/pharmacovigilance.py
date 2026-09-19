import logging
import random
import string
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.pharmacovigilance import AdverseEvent, SeriousAdverseEvent, CausalityAssessment, SafetySignal
from app.schemas.pharmacovigilance import AdverseEventCreate, AdverseEventUpdate, SAECreate, SAEUpdate, CausalityAssessmentCreate, AdverseEventOut, SAEOut, SafetySignalOut
from typing import List, Optional

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pharmacovigilance", tags=["Pharmacovigilance"])



def _ae_out(ae: AdverseEvent) -> AdverseEventOut:
    """Serialize an AdverseEvent ORM instance, resolving the drug name from the relationship."""
    data = AdverseEventOut.model_validate(ae)
    if ae.suspected_drug:
        data.suspected_drug_name = ae.suspected_drug.name
    return data


@router.get("/adverse-events", response_model=List[AdverseEventOut])
async def list_aes(trial_id: Optional[str] = None, severity: Optional[str] = None, seriousness: Optional[str] = None, status: Optional[str] = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(AdverseEvent).where(AdverseEvent.is_deleted == False)
    if trial_id:
        query = query.where(AdverseEvent.trial_id == trial_id)
    if severity:
        query = query.where(AdverseEvent.severity == severity)
    if seriousness:
        query = query.where(AdverseEvent.seriousness == seriousness)
    if status:
        query = query.where(AdverseEvent.status == status)
    result = await db.execute(query.order_by(AdverseEvent.reported_date.desc()).offset(skip).limit(limit))
    return [_ae_out(ae) for ae in result.scalars().all()]

@router.post("/adverse-events", response_model=AdverseEventOut)
async def create_ae(data: AdverseEventCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR", "PHARMACOVIGILANCE_OFFICER"))):
    ae = AdverseEvent(**data.model_dump(), reporter_id=current_user.id, reported_date=date.today(), status="REPORTED")
    db.add(ae)
    await db.commit()
    await db.refresh(ae)
    return _ae_out(ae)

@router.put("/adverse-events/{ae_id}", response_model=AdverseEventOut)
async def update_ae(ae_id: str, data: AdverseEventUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "PHARMACOVIGILANCE_OFFICER"))):
    result = await db.execute(select(AdverseEvent).where(AdverseEvent.id == ae_id))
    ae = result.scalar_one_or_none()
    if not ae:
        raise HTTPException(status_code=404, detail="Adverse event not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ae, key, value)
    await db.commit()
    await db.refresh(ae)
    return _ae_out(ae)

@router.get("/serious-adverse-events", response_model=List[SAEOut])
async def list_saes(status: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(SeriousAdverseEvent)
    if status:
        query = query.where(SeriousAdverseEvent.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/serious-adverse-events", response_model=SAEOut)
async def create_sae(data: SAECreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "PHARMACOVIGILANCE_OFFICER"))):
    sae_num = "SAE-" + "".join(random.choices(string.digits, k=6))
    sae = SeriousAdverseEvent(**data.model_dump(), sae_number=sae_num, status="REPORTED")
    db.add(sae)
    # Update AE seriousness
    result = await db.execute(select(AdverseEvent).where(AdverseEvent.id == data.adverse_event_id))
    ae = result.scalar_one_or_none()
    if ae:
        ae.seriousness = "SERIOUS"
    await db.commit()
    await db.refresh(sae)
    return sae

@router.put("/serious-adverse-events/{sae_id}", response_model=SAEOut)
async def update_sae(sae_id: str, data: SAEUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PHARMACOVIGILANCE_OFFICER"))):
    result = await db.execute(select(SeriousAdverseEvent).where(SeriousAdverseEvent.id == sae_id))
    sae = result.scalar_one_or_none()
    if not sae:
        raise HTTPException(status_code=404, detail="SAE not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sae, key, value)
    await db.commit()
    return sae

@router.get("/safety-signals", response_model=List[SafetySignalOut])
async def list_safety_signals(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(SafetySignal)
    if trial_id:
        query = query.where(SafetySignal.trial_id == trial_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/summary")
async def safety_summary(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    ae_q = select(func.count()).select_from(AdverseEvent).where(AdverseEvent.is_deleted == False)
    sae_q = select(func.count()).select_from(SeriousAdverseEvent)
    if trial_id:
        ae_q = ae_q.where(AdverseEvent.trial_id == trial_id)
    total_aes = (await db.execute(ae_q)).scalar() or 0
    total_saes = (await db.execute(sae_q)).scalar() or 0
    open_saes = (await db.execute(select(func.count()).select_from(SeriousAdverseEvent).where(SeriousAdverseEvent.status != "CLOSED"))).scalar() or 0
    # Severity breakdown
    mild = (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "MILD"))).scalar() or 0
    moderate = (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "MODERATE"))).scalar() or 0
    severe = (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "SEVERE"))).scalar() or 0
    return {"total_aes": total_aes, "total_saes": total_saes, "open_saes": open_saes, "by_severity": {"mild": mild, "moderate": moderate, "severe": severe}}
