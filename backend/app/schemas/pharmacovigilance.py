from pydantic import BaseModel
from typing import Optional
from datetime import date

class AdverseEventCreate(BaseModel):
    participant_id: str
    trial_id: str
    site_id: Optional[str] = None
    event_term: str
    description: Optional[str] = None
    onset_date: Optional[date] = None
    severity: str = "MILD"
    seriousness: str = "NON_SERIOUS"
    causality: str = "POSSIBLE"
    expectedness: str = "EXPECTED"
    action_taken: Optional[str] = None
    outcome: str = "UNKNOWN"
    suspected_causative_drug_id: Optional[str] = None

class AdverseEventUpdate(BaseModel):
    resolution_date: Optional[date] = None
    severity: Optional[str] = None
    seriousness: Optional[str] = None
    causality: Optional[str] = None
    outcome: Optional[str] = None
    status: Optional[str] = None
    action_taken: Optional[str] = None
    suspected_causative_drug_id: Optional[str] = None

class SAECreate(BaseModel):
    adverse_event_id: str
    criteria: Optional[str] = None
    narrative: Optional[str] = None

class SAEUpdate(BaseModel):
    status: Optional[str] = None
    reported_to_sponsor_date: Optional[date] = None
    reported_to_ethics_date: Optional[date] = None
    reported_to_regulatory_date: Optional[date] = None
    narrative: Optional[str] = None

class CausalityAssessmentCreate(BaseModel):
    adverse_event_id: str
    method: Optional[str] = None
    causality_rating: Optional[str] = None
    rationale: Optional[str] = None

class AdverseEventOut(BaseModel):
    id: str
    participant_id: str
    trial_id: str
    event_term: str
    description: Optional[str] = None
    onset_date: Optional[date] = None
    resolution_date: Optional[date] = None
    severity: str
    seriousness: str
    causality: str
    expectedness: str
    outcome: str
    status: str
    reported_date: Optional[date] = None
    suspected_causative_drug_id: Optional[str] = None
    suspected_drug_name: Optional[str] = None  # resolved from the relationship

    class Config:
        from_attributes = True

class SAEOut(BaseModel):
    id: str
    adverse_event_id: str
    sae_number: Optional[str] = None
    criteria: Optional[str] = None
    narrative: Optional[str] = None
    status: str
    reported_to_sponsor_date: Optional[date] = None
    reported_to_ethics_date: Optional[date] = None
    class Config:
        from_attributes = True

class SafetySignalOut(BaseModel):
    id: str
    trial_id: str
    signal_term: str
    description: Optional[str] = None
    detected_date: Optional[date] = None
    status: str
    severity: Optional[str] = None
    class Config:
        from_attributes = True
