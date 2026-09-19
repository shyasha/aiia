# Graph Report - aiia  (2026-09-19)

## Corpus Check
- 153 files · ~62,336 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 4, .example 3, .ini 1)

## Summary
- 920 nodes · 2406 edges · 64 communities (44 shown, 20 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 258 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `db1ab351`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- BaseModel
- sites.py
- react
- AIIA Clinical Trials Dashboard (CTMS)
- v1/auth.py
- MemoryExtractionPipeline
- participants.py
- test_memory_system.py
- forms.py
- v1/ethics.py
- build_context
- api.ts
- v1/regulatory.py
- trials.py
- demo-record-panel.tsx
- package.json
- compilerOptions
- visits.py
- memory.py
- os
- GraphifyAdapter
- Participant Entities
- typing
- schemas/fhir.py
- Passlib Bcrypt Password Hashing
- API Layer (FastAPI Routes)
- v1/pharmacovigilance.py
- Graphify Knowledge Graph Rules
- SQLAlchemy Async Dependency
- next
- security.py
- logging
- copilot/page.tsx
- database.py
- sidebar.tsx
- next.config.js
- env.py
- memory/__init__.py
- sqlalchemy
- .after_agent_turn
- v1/cdisc.py
- upload_document
- UUID Primary Keys
- next-env.d.ts
- test_e2e.py
- Analytics Endpoints
- Sites Endpoints
- Users Endpoints
- Visits Endpoints
- Soft Deletes Pattern
- Environment Secrets Management
- Settings
- analytics/page.tsx
- guide/page.tsx
- list_notifications
- rate_limit.py
- log_requests

## God Nodes (most connected - your core abstractions)
1. `BaseModel` - 145 edges
2. `seed_data()` - 38 edges
3. `Participant` - 29 edges
4. `get_current_user()` - 26 edges
5. `GraphifyAdapter` - 24 edges
6. `react` - 24 edges
7. `AdverseEvent` - 22 edges
8. `build_context()` - 21 edges
9. `TenantGraphStorage` - 21 edges
10. `get_db()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Bcrypt Password Hashing` --implements--> `Passlib Bcrypt Password Hashing`  [INFERRED]
  docs/security.md → backend/requirements.txt
- `JWT-Based Authentication` --implements--> `Python Jose JWT`  [INFERRED]
  docs/security.md → backend/requirements.txt
- `Async-First Architecture` --rationale_for--> `Asyncpg PostgreSQL Driver`  [INFERRED]
  docs/architecture.md → backend/requirements.txt
- `Async-First Architecture` --rationale_for--> `SQLAlchemy Async Dependency`  [INFERRED]
  docs/architecture.md → backend/requirements.txt
- `FastAPI Backend` --implements--> `FastAPI Dependency`  [INFERRED]
  README.md → backend/requirements.txt

## Import Cycles
- None detected.

## Communities (64 total, 20 thin omitted)

### Community 0 - "BaseModel"
Cohesion: 0.12
Nodes (51): get_dashboard(), AsyncSession, get, global_search(), AsyncSession, get, AuditLog, Append-only audit log - no updates or deletes. (+43 more)

### Community 1 - "sites.py"
Cohesion: 0.23
Nodes (18): create_investigator(), create_site(), create_site_assignment(), get_site(), list_investigators(), list_sites(), AsyncSession, get (+10 more)

### Community 2 - "react"
Cohesion: 0.18
Nodes (14): AuditPage(), ParticipantDetail(), ParticipantsPage(), EMPTY_FORM, Intervention, PharmacovigilancePage(), Trial, SitesPage() (+6 more)

### Community 3 - "AIIA Clinical Trials Dashboard (CTMS)"
Cohesion: 0.05
Nodes (43): FastAPI Dependency, Pydantic Schema Validation, Uvicorn ASGI Server, Docker Compose Backend Service, Docker Compose Frontend Service, Docker Compose Postgres Service, Audit Trail Endpoints, CDISC Export Endpoints (+35 more)

### Community 4 - "v1/auth.py"
Cohesion: 0.12
Nodes (36): get_me(), login(), logout(), AsyncSession, get, post, refresh_token(), set_auth_cookies() (+28 more)

### Community 5 - "MemoryExtractionPipeline"
Cohesion: 0.16
Nodes (23): app_memory_types_enums, MemoryExtractionPipeline, Extracts entities, preferences, facts, events, and relationships from text or…, Extract entities, preferences, facts, and relationships from a message., ConfidenceLevel, EntityType, MemoryType, RelationType (+15 more)

### Community 6 - "participants.py"
Cohesion: 0.13
Nodes (31): get_adverse_event(), get_observation(), get_patient(), get_research_study(), get_research_subject(), AsyncSession, get, count_participants() (+23 more)

### Community 7 - "test_memory_system.py"
Cohesion: 0.09
Nodes (27): app_memory_context_builder, app_memory_extraction_pipeline, app_memory_graph_adapter, app_memory_graph_storage, app_memory_middleware_lifecycle, Populate seed memory graphs for demo users., seed_demo_data(), Any (+19 more)

### Community 8 - "forms.py"
Cohesion: 0.17
Nodes (25): create_data_query(), create_form(), create_form_field(), create_submission(), get_form_fields(), list_data_queries(), list_forms(), list_submissions() (+17 more)

### Community 9 - "v1/ethics.py"
Cohesion: 0.20
Nodes (19): create_approval(), create_committee(), create_submission(), list_approvals(), list_committees(), list_submissions(), AsyncSession, get (+11 more)

### Community 10 - "build_context"
Cohesion: 0.13
Nodes (17): app_memory_ranking_ranker, app_memory_retrieval_search, build_context(), Any, Build structured context package for a given user message. Returns dictionary…, MultiFactorRanker, Any, Graph (+9 more)

### Community 11 - "api.ts"
Cohesion: 0.14
Nodes (10): DashboardLayout(), LoginPage(), Home(), Topbar(), getUser(), isAuthenticated(), login(), logout() (+2 more)

### Community 12 - "v1/regulatory.py"
Cohesion: 0.22
Nodes (17): create_checklist_item(), create_record(), list_checklists(), list_records(), AsyncSession, get, post, put (+9 more)

### Community 13 - "trials.py"
Cohesion: 0.19
Nodes (21): create_study_arm(), create_trial(), get_trial(), get_trial_arms(), get_trial_interventions(), list_trials(), AsyncSession, get (+13 more)

### Community 14 - "demo-record-panel.tsx"
Cohesion: 0.16
Nodes (4): DemoRecord, DemoRecordPanel(), RECORD_NAV, RecordItem

### Community 15 - "package.json"
Cohesion: 0.04
Nodes (45): dependencies, axios, clsx, date-fns, @hookform/resolvers, lucide-react, next, react (+37 more)

### Community 16 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 17 - "visits.py"
Cohesion: 0.23
Nodes (15): create_participant_visit(), create_visit_definition(), list_participant_visits(), list_visit_definitions(), AsyncSession, get, post, put (+7 more)

### Community 18 - "memory.py"
Cohesion: 0.22
Nodes (15): app_memory_privacy_isolation, api_build_context(), api_decay(), api_delete_node(), api_forget(), api_get_nodes(), api_ingest_memory(), ContextRequest (+7 more)

### Community 19 - "os"
Cohesion: 0.06
Nodes (21): anthropic, AsyncAnthropic, asyncio, ask_claude(), _assess_ae_risk_standalone(), _get_client(), Call Claude and return the text response. Raises RuntimeError on API failure so…, Build an AE risk prompt, call Claude, parse the JSON response. Args: ae_data:… (+13 more)

### Community 20 - "GraphifyAdapter"
Cohesion: 0.11
Nodes (19): GraphifyAdapter, Any, Graph, Adapter encapsulating Graphify SDK / NetworkX graph operations. Keeps all…, Validate extraction dict against Graphify's official schema., Raise ValueError if extraction dict violates Graphify schema., Build NetworkX graph using Graphify's official build mechanism., Export a NetworkX graph into Graphify-compliant extraction dict format. (+11 more)

### Community 21 - "Participant Entities"
Cohesion: 0.22
Nodes (9): Audit Log & System Entities, Ethics Committee Entities, eCRF / EDC Entities, Participant Entities, Pharmacovigilance Entities, Regulatory Tracking Entities, Sites & Investigators Entities, Trial Management Entities (+1 more)

### Community 22 - "typing"
Cohesion: 0.17
Nodes (13): list_audit_logs(), AsyncSession, get, AuditLogOut, Config, Config, DocumentCreate, DocumentOut (+5 more)

### Community 23 - "schemas/fhir.py"
Cohesion: 0.52
Nodes (6): FHIRAdverseEvent, FHIRObservation, FHIRPatient, FHIRResearchStudy, FHIRResearchSubject, FHIRResource

### Community 24 - "Passlib Bcrypt Password Hashing"
Cohesion: 0.33
Nodes (6): Passlib Bcrypt Password Hashing, Python Jose JWT, Auth Endpoints, API Authentication, Bcrypt Password Hashing, JWT-Based Authentication

### Community 25 - "API Layer (FastAPI Routes)"
Cohesion: 0.33
Nodes (6): API Layer (FastAPI Routes), Model Layer (SQLAlchemy ORM), Schema Layer (Pydantic Validation), Service Layer (Business Logic), Three-Tier Architecture Overview, Backend Permission Enforcement

### Community 26 - "v1/pharmacovigilance.py"
Cohesion: 0.14
Nodes (29): export_cdisc(), list_mappings(), AsyncSession, get, post, _ae_out(), create_ae(), create_sae() (+21 more)

### Community 27 - "Graphify Knowledge Graph Rules"
Cohesion: 0.50
Nodes (4): Graphify Knowledge Graph Rules, Graphify CLI Query, Graphify Subgraph Navigation, Graphify Pipeline Workflow

### Community 28 - "SQLAlchemy Async Dependency"
Cohesion: 0.67
Nodes (4): Alembic Migration Tool, Asyncpg PostgreSQL Driver, SQLAlchemy Async Dependency, Async-First Architecture

### Community 29 - "next"
Cohesion: 0.10
Nodes (8): items, metadata, frontend_app_globals, metadata, metadata, metadata, CookieConsent(), next

### Community 30 - "security.py"
Cohesion: 0.20
Nodes (10): ChecklistToggle, get_demo_record(), get_demo_records(), get, get_current_user(), AsyncSession, Request, bcrypt (+2 more)

### Community 31 - "logging"
Cohesion: 0.28
Nodes (6): app_memory_types_models, hashlib, logging, math, networkx, pathlib

### Community 32 - "copilot/page.tsx"
Cohesion: 0.18
Nodes (9): alertTypeIcon(), CopilotPage(), entityLabel(), severityConfig(), WorkflowAlert, secondaryCards, triadCards, record (+1 more)

### Community 33 - "database.py"
Cohesion: 0.15
Nodes (15): Base, get_db(), health_check(), lifespan(), get, readiness_check(), contextlib, DeclarativeBase (+7 more)

### Community 34 - "sidebar.tsx"
Cohesion: 0.50
Nodes (4): demoWorkflows, mainNav, Sidebar(), cn()

### Community 36 - "env.py"
Cohesion: 0.09
Nodes (14): alembic, downgrade(), Create workflow_alerts table for the AI Co-Pilot feature., Drop workflow_alerts table., upgrade(), downgrade(), Drop AI clinical risk fields — replaced by workflow_alerts table., Restore AI clinical risk fields. (+6 more)

### Community 38 - "sqlalchemy"
Cohesion: 0.14
Nodes (19): Config, list_alerts(), AsyncSession, get, post, Workflow Alerts API — AI Co-Pilot endpoints. POST /workflow-alerts/scan —…, Trigger a workflow health scan and regenerate alerts., Return all current workflow alerts sorted by severity (high first). (+11 more)

### Community 39 - ".after_agent_turn"
Cohesion: 0.40
Nodes (3): Any, Step 1 & 2: Retrieve relevant graph memory & build structured context., Step 4, 5, 6: Extract new memories, validate + deduplicate, and persist to…

### Community 40 - "v1/cdisc.py"
Cohesion: 0.32
Nodes (5): require_roles(), CDISCExportRequest, CDISCMappingOut, Config, fastapi_responses

### Community 41 - "upload_document"
Cohesion: 0.33
Nodes (6): list_documents(), AsyncSession, get, post, upload_document(), UploadFile

### Community 56 - "Settings"
Cohesion: 0.33
Nodes (4): Settings, BaseSettings, field_validator, model_validator

### Community 60 - "list_notifications"
Cohesion: 0.38
Nodes (7): list_notifications(), mark_all_read(), mark_as_read(), AsyncSession, get, put, unread_count()

### Community 61 - "rate_limit.py"
Cohesion: 0.29
Nodes (4): InMemoryRateLimiter, collections, threading, time

### Community 62 - "log_requests"
Cohesion: 0.67
Nodes (3): log_requests(), Request, middleware

## Knowledge Gaps
- **117 isolated node(s):** `Config`, `Config`, `Config`, `Config`, `Config` (+112 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 304 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseModel` connect `BaseModel` to `sites.py`, `v1/auth.py`, `MemoryExtractionPipeline`, `participants.py`, `forms.py`, `v1/ethics.py`, `build_context`, `v1/regulatory.py`, `trials.py`, `visits.py`, `memory.py`, `GraphifyAdapter`, `typing`, `schemas/fhir.py`, `v1/pharmacovigilance.py`, `security.py`, `database.py`, `sqlalchemy`, `v1/cdisc.py`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `build_context()` connect `build_context` to `MemoryExtractionPipeline`, `.after_agent_turn`, `test_memory_system.py`, `memory.py`, `GraphifyAdapter`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `TenantGraphStorage` connect `test_memory_system.py` to `memory.py`, `build_context`, `GraphifyAdapter`, `logging`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **What connects `Config`, `Config`, `Config` to the rest of the system?**
  _117 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `BaseModel` be split into smaller, more focused modules?**
  _Cohesion score 0.12361466325660699 - nodes in this community are weakly interconnected._
- **Should `AIIA Clinical Trials Dashboard (CTMS)` be split into smaller, more focused modules?**
  _Cohesion score 0.05094130675526024 - nodes in this community are weakly interconnected._
- **Should `v1/auth.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11923076923076924 - nodes in this community are weakly interconnected._