# AIIA Clinical Trial Management System (CTMS)

A web-based Clinical Trial Management System (CTMS) designed for Ayurveda clinical research, supporting protocol lifecycle tracking, participant management, adverse event surveillance, and workflow health monitoring.

Built with **FastAPI**, **Next.js**, **SQLAlchemy**, and **PostgreSQL/SQLite**, the platform demonstrates standardized clinical trial workflows with CDISC SDTM domain mapping, FHIR R4 interoperability, and an operational AI co-pilot for process tracking.

---

## System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                       Client Browser                        │
│   Investigators │ Study Coordinators │ PV Officers │ Admins │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│            Frontend Application (Next.js 14 / React)        │
│    App Router │ TypeScript │ Tailwind CSS │ Responsive UI   │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / REST (JSON)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             Backend API Services (FastAPI / Python)         │
│   Authentication (JWT/RBAC) │ Pydantic Validation │ OpenAPI │
├──────────────────────────────┬──────────────────────────────┤
│  Core CTMS                   │ Safety & Workflow            │
│  - Trials & Interventions    │ - Pharmacovigilance (AE/SAE) │
│  - Participants & Consent    │ - Operational AI Co-Pilot    │
│  - Visits & Milestones       │ - Audit Logging & CDISC/FHIR │
└──────────────────────────────┬──────────────────────────────┘
                               │ Async ORM (SQLAlchemy 2.0)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     Database Layer                          │
│    PostgreSQL 16 (Production) / SQLite + aiosqlite (Dev)    │
│    Alembic Migrations │ Soft Deletes │ Relational Schema    │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

- **Frontend**: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide React, Axios
- **Backend**: FastAPI, Python 3.11+, SQLAlchemy 2.0 (Async), Pydantic v2, Alembic
- **Database**: 
  - Local Development: SQLite via `aiosqlite` (zero-dependency setup)
  - Production / Staging: PostgreSQL 16 via `asyncpg`
- **AI Integration**: Anthropic Claude API (`ask_claude`) for non-clinical operational bottleneck detection and alert message phrasing
- **Standards & Formats**: CDISC SDTM dataset export (DM, SV, AE), FHIR R4 resource representations

---

## Core Capabilities

### 1. Trial & Protocol Lifecycle Management
- Structured trial registry tracking phase, therapeutic area, Ayurveda system, study arms, and planned sample sizes.
- Intervention catalog: formulation, dosage, duration, and route administration records per trial.
- Milestone tracking: protocol clearance, ethics approval, recruitment targets, and completion milestones.

### 2. Participant & Visit Tracking
- Participant enrollment with automated pseudonymous trial identifiers (`AIIA-001-xxx`).
- Informed consent recording and eligibility screening logs.
- Longitudinal visit schedules with automated overdue detection and window calculations.

### 3. Pharmacovigilance & Safety Surveillance
- Adverse Event (AE) and Serious Adverse Event (SAE) reporting with CTCAE-style severity classification.
- **Suspected Causative Drug / Intervention Attribution**: Allows coordinators and clinicians to link reported AEs directly to registered trial interventions via foreign key relationships.
- WHO-UMC causality assessment logging and regulatory escalation tracking.

### 4. AI Operational Co-Pilot
- Continuous process monitor that scans:
  - Adverse Events pending clinical review beyond the standard 5-day review window.
  - Scheduled participant visits that have passed their target date.
  - Trial milestones approaching deadline within 7 days or past due.
- Claude-powered alert generation: translates operational data into clear, actionable, non-clinical alert notifications categorized by severity (`high`, `medium`, `low`).
- Dedicated AI Co-Pilot dashboard (`/dashboard/copilot`) with manual on-demand health scan triggers.

### 5. Standards, Auditability & Interoperability
- **CDISC SDTM Export**: Serializes trial records into standard clinical data domains (Demographics `DM`, Subject Visits `SV`, Adverse Events `AE`).
- **FHIR R4 Interfaces**: RESTful endpoints exposing Patient, ResearchStudy, ResearchSubject, Observation, and AdverseEvent resources.
- **Append-Only Audit Trail**: Captures user actions, timestamps, affected entities, and state changes for compliance tracing.

---

## Local Development Setup

### Prerequisites
- **Python 3.11+**
- **Node.js 20+** and **npm**
- (Optional) **Docker & Docker Compose** for containerized PostgreSQL execution

---

### Option A: Local Run (Quick Start with SQLite)

The default `.env` configuration in `backend/` uses SQLite, enabling local execution without installing an external database engine.

#### 1. Backend Setup

```bash
cd backend

# Create and activate a Python virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be accessible at [http://localhost:8000](http://localhost:8000). Interactive Swagger documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

#### 2. Frontend Setup

In a separate terminal:

```bash
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

The frontend application will be live at [http://localhost:3000](http://localhost:3000).

---

### Option B: Docker Compose (PostgreSQL Full Stack)

To run the complete stack with a dedicated PostgreSQL 16 container:

```bash
# From the repository root
cp .env.example .env

# Build and launch all containers
docker compose up --build
```

Docker Compose spins up:
- `postgres`: PostgreSQL 16 container running on port `5432`
- `backend`: FastAPI application on port `8000` (auto-applies migrations on launch)
- `frontend`: Next.js web application on port `3000`

---

## Demo Accounts & Roles

The system uses Role-Based Access Control (RBAC) enforced via JWT tokens and HTTP cookies. For evaluation and demo walkthroughs, pre-configured accounts are provided:

| Role | Email | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@aiia.gov.in` | `Demo@12345` | Global administrative control, demo walkthrough, system config |
| **Trial Admin** | `trialadmin@aiia.gov.in` | `Demo@12345` | Trial creation, protocol amendments, site allocations |
| **Principal Investigator** | `pi@aiia.gov.in` | `Demo@12345` | Subject eligibility clearance, medical evaluations, AE reporting |
| **Study Coordinator** | `coordinator@aiia.gov.in` | `Demo@12345` | Subject visits, eCRF data entry, operational scheduling |
| **Pharmacovigilance Officer** | `pv@aiia.gov.in` | `Demo@12345` | Safety review, causality assessment, regulatory notifications |
| **Data Manager** | `datamanager@aiia.gov.in` | `Demo@12345` | Data validation queries, CDISC / SDTM exports |
| **Ethics Committee** | `ethics@aiia.gov.in` | `Demo@12345` | IEC submission review, approval certifications |
| **Auditor / Viewer** | `auditor@aiia.gov.in` | `Demo@12345` | Read-only inspection of audit logs and trial records |

---

## Repository Structure

```text
aiia-ctms/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST route handlers (trials, visits, pharmacovigilance, copilot)
│   │   ├── core/            # Database engine, JWT authentication, configuration
│   │   ├── models/          # SQLAlchemy relational models
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # Business logic (Claude wrapper, workflow scanner)
│   │   ├── seed.py          # Database seeder script
│   │   └── main.py          # FastAPI application entry point
│   ├── migrations/          # Alembic database version scripts
│   ├── tests/               # Backend pytest test suite
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container specification
├── frontend/
│   ├── app/
│   │   ├── dashboard/       # Dashboard pages (overview, trials, participants, PV, copilot)
│   │   ├── login/           # Authentication login page
│   │   └── layout.tsx       # Root layout and theme providers
│   ├── components/          # Reusable UI widgets and layout navigation
│   ├── lib/                 # Axios client, date formatters, auth session helpers
│   ├── package.json         # Frontend dependencies and scripts
│   └── Dockerfile           # Frontend container specification
├── docker-compose.yml       # Multi-container orchestration definition
└── README.md                # Project documentation
```

---

## Verification & Testing

### Running Tests

```bash
# Backend unit and schema test suite
cd backend
python -m pytest -v

# Frontend TypeScript type verification
cd frontend
npx tsc --noEmit
```

---

## Academic Research Disclaimer

This project was developed as an academic software engineering demonstration of Clinical Trial Management Systems for Ayurveda research. While designed in alignment with Good Clinical Practice (GCP) principles and Indian New Drugs and Clinical Trials (NDCT) Rules 2019 data structures, **this system is not certified as medical device software or a legally certified regulatory submission repository**. The operational AI assistant provides workflow tracking and does not perform medical diagnosis or clinical decision-making.
