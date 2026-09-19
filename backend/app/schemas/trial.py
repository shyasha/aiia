from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class TrialCreate(BaseModel):
    title: str
    short_title: Optional[str] = None
    protocol_number: Optional[str] = None
    registration_number: Optional[str] = None
    phase: Optional[str] = None
    study_type: Optional[str] = None
    intervention_type: Optional[str] = None
    therapeutic_area: Optional[str] = None
    ayurveda_system: Optional[str] = None
    primary_objective: Optional[str] = None
    secondary_objectives: Optional[str] = None
    inclusion_criteria: Optional[str] = None
    exclusion_criteria: Optional[str] = None
    planned_sample_size: Optional[int] = None
    sponsor: Optional[str] = None
    pi_id: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    status: str = "PLANNING"
    description: Optional[str] = None

class TrialUpdate(BaseModel):
    title: Optional[str] = None
    short_title: Optional[str] = None
    protocol_number: Optional[str] = None
    registration_number: Optional[str] = None
    phase: Optional[str] = None
    study_type: Optional[str] = None
    intervention_type: Optional[str] = None
    therapeutic_area: Optional[str] = None
    ayurveda_system: Optional[str] = None
    primary_objective: Optional[str] = None
    secondary_objectives: Optional[str] = None
    inclusion_criteria: Optional[str] = None
    exclusion_criteria: Optional[str] = None
    planned_sample_size: Optional[int] = None
    sponsor: Optional[str] = None
    pi_id: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    status: Optional[str] = None
    description: Optional[str] = None

class StudyArmCreate(BaseModel):
    name: str
    description: Optional[str] = None
    allocation_ratio: float = 1.0
    arm_type: str = "TREATMENT"

class InterventionCreate(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[str] = None
    formulation: Optional[str] = None

class MilestoneCreate(BaseModel):
    name: str
    planned_date: Optional[date] = None
    status: str = "PENDING"
    notes: Optional[str] = None

class TrialOut(BaseModel):
    id: str
    title: str
    short_title: Optional[str] = None
    protocol_number: Optional[str] = None
    registration_number: Optional[str] = None
    phase: Optional[str] = None
    study_type: Optional[str] = None
    intervention_type: Optional[str] = None
    therapeutic_area: Optional[str] = None
    ayurveda_system: Optional[str] = None
    primary_objective: Optional[str] = None
    planned_sample_size: Optional[int] = None
    sponsor: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    status: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    site_count: int = 0
    participant_count: int = 0

    class Config:
        from_attributes = True

class StudyArmOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    allocation_ratio: float = 1.0
    arm_type: str = "TREATMENT"
    class Config:
        from_attributes = True

class InterventionOut(BaseModel):
    id: str
    trial_id: str
    name: str
    type: Optional[str] = None
    dosage: Optional[str] = None
    formulation: Optional[str] = None
    class Config:
        from_attributes = True
