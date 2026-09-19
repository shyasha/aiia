from fastapi import APIRouter
from app.api.v1 import auth, users, trials, sites, participants, visits, forms, ethics, regulatory, pharmacovigilance, documents, audit, notifications, analytics, cdisc, fhir, search, memory, demo, workflow_alerts

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(trials.router)
api_router.include_router(sites.router)
api_router.include_router(participants.router)
api_router.include_router(visits.router)
api_router.include_router(forms.router)
api_router.include_router(ethics.router)
api_router.include_router(regulatory.router)
api_router.include_router(pharmacovigilance.router)
api_router.include_router(documents.router)
api_router.include_router(audit.router)
api_router.include_router(notifications.router)
api_router.include_router(analytics.router)
api_router.include_router(cdisc.router)
api_router.include_router(fhir.router)
api_router.include_router(search.router)
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(demo.router)
api_router.include_router(workflow_alerts.router)

