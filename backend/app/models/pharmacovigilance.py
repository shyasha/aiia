from sqlalchemy import Column, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class AdverseEvent(BaseModel):
    __tablename__ = "adverse_events"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=True)
    event_term = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    onset_date = Column(Date, nullable=True)
    resolution_date = Column(Date, nullable=True)
    severity = Column(String(20), default="MILD")  # MILD, MODERATE, SEVERE
    seriousness = Column(String(20), default="NON_SERIOUS")  # NON_SERIOUS, SERIOUS
    causality = Column(String(20), default="POSSIBLE")
    # UNRELATED, UNLIKELY, POSSIBLE, PROBABLE, DEFINITE
    expectedness = Column(String(20), default="EXPECTED")  # EXPECTED, UNEXPECTED
    action_taken = Column(Text, nullable=True)
    outcome = Column(String(30), default="UNKNOWN")
    # RECOVERED, RECOVERING, NOT_RECOVERED, FATAL, UNKNOWN
    reporter_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    reported_date = Column(Date, nullable=True)
    status = Column(String(20), default="REPORTED", index=True)
    # Manually recorded by coordinator/investigator — NOT AI-generated
    suspected_causative_drug_id = Column(String(36), ForeignKey("interventions.id"), nullable=True)

    participant = relationship("Participant", back_populates="adverse_events")
    trial = relationship("Trial")
    site = relationship("Site")
    suspected_drug = relationship("Intervention", lazy="selectin")

class SeriousAdverseEvent(BaseModel):
    __tablename__ = "serious_adverse_events"
    adverse_event_id = Column(String(36), ForeignKey("adverse_events.id"), nullable=False, index=True)
    sae_number = Column(String(20), nullable=True, unique=True)
    criteria = Column(String(30), nullable=True)
    # DEATH, LIFE_THREATENING, HOSPITALIZATION, DISABILITY, CONGENITAL_ANOMALY, OTHER
    narrative = Column(Text, nullable=True)
    reported_to_sponsor_date = Column(Date, nullable=True)
    reported_to_ethics_date = Column(Date, nullable=True)
    reported_to_regulatory_date = Column(Date, nullable=True)
    status = Column(String(30), default="REPORTED", index=True)
    # REPORTED, UNDER_REVIEW, MEDICAL_REVIEW, REGULATORY_REVIEW, SUBMITTED, CLOSED
    
    adverse_event = relationship("AdverseEvent")

class CausalityAssessment(BaseModel):
    __tablename__ = "causality_assessments"
    adverse_event_id = Column(String(36), ForeignKey("adverse_events.id"), nullable=False, index=True)
    assessor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    assessment_date = Column(Date, nullable=True)
    method = Column(String(50), nullable=True)  # WHO-UMC, Naranjo
    causality_rating = Column(String(20), nullable=True)
    rationale = Column(Text, nullable=True)
    
    adverse_event = relationship("AdverseEvent")

class SafetySignal(BaseModel):
    __tablename__ = "safety_signals"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    signal_term = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    detected_date = Column(Date, nullable=True)
    status = Column(String(20), default="DETECTED")  # DETECTED, UNDER_REVIEW, CONFIRMED, CLOSED
    severity = Column(String(20), nullable=True)
    action_taken = Column(Text, nullable=True)
    
    trial = relationship("Trial")
