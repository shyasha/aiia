"""Comprehensive seed data for AIIA CTMS demo."""
import asyncio
import random
import string
from datetime import date, datetime, timedelta, timezone
from app.core.database import AsyncSessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, Role, Permission, UserRole, RolePermission
from app.models.trial import Trial, Protocol, StudyArm, Intervention, TrialMilestone
from app.models.site import Site, Investigator, SiteAssignment
from app.models.participant import Participant, Consent, Screening, Enrollment, Randomization
from app.models.visit import VisitDefinition, ParticipantVisit
from app.models.form import Form, FormField, FormSubmission, DataQuery
from app.models.ethics import EthicsCommittee, EthicsSubmission, EthicsReview, EthicsApproval
from app.models.regulatory import RegulatoryRecord, RegulatoryChecklist
from app.models.pharmacovigilance import AdverseEvent, SeriousAdverseEvent, CausalityAssessment, SafetySignal
from app.models.document import Document
from app.models.audit import AuditLog
from app.models.notification import Notification
from app.models.cdisc import CDISCMapping

def rand_id():
    return "".join(random.choices(string.digits, k=6))

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        print("Seeding roles...")
        role_names = [
            ("SUPER_ADMIN", "Full system access"),
            ("TRIAL_ADMIN", "Manage trials, sites, users and configuration"),
            ("PRINCIPAL_INVESTIGATOR", "Manage assigned trials, participants, clinical data"),
            ("STUDY_COORDINATOR", "Participant enrollment, visits, forms"),
            ("DATA_MANAGER", "Clinical data, validation, CDISC exports"),
            ("ETHICS_COMMITTEE", "Ethics submissions, reviews, approvals"),
            ("PHARMACOVIGILANCE_OFFICER", "AE/SAE management, safety signals"),
            ("REGULATORY_OFFICER", "CTRI tracking, regulatory compliance"),
            ("AUDITOR", "Read-only access to all records and audit trails"),
            ("VIEWER", "Read-only dashboard access"),
        ]
        roles = {}
        for name, desc in role_names:
            r = Role(name=name, description=desc, is_system_role=True)
            db.add(r)
            roles[name] = r
        await db.flush()
        
        print("Seeding users...")
        pwd = get_password_hash("Demo@12345")
        users_data = [
            ("admin@aiia.gov.in", "admin", "Dr. Rajesh Kumar", True, "SUPER_ADMIN"),
            ("trialadmin@aiia.gov.in", "trialadmin", "Dr. Priya Sharma", False, "TRIAL_ADMIN"),
            ("pi@aiia.gov.in", "pi", "Dr. Anil Gupta", False, "PRINCIPAL_INVESTIGATOR"),
            ("coordinator@aiia.gov.in", "coordinator", "Meera Patel", False, "STUDY_COORDINATOR"),
            ("datamanager@aiia.gov.in", "datamanager", "Rahul Singh", False, "DATA_MANAGER"),
            ("ethics@aiia.gov.in", "ethics", "Prof. Sunita Devi", False, "ETHICS_COMMITTEE"),
            ("pv@aiia.gov.in", "pv", "Dr. Vikram Joshi", False, "PHARMACOVIGILANCE_OFFICER"),
            ("regulatory@aiia.gov.in", "regulatory", "Kavita Reddy", False, "REGULATORY_OFFICER"),
            ("auditor@aiia.gov.in", "auditor", "Suresh Nair", False, "AUDITOR"),
            ("viewer@aiia.gov.in", "viewer", "Anjali Menon", False, "VIEWER"),
        ]
        users = {}
        for email, uname, fname, is_super, role_name in users_data:
            u = User(email=email, username=uname, full_name=fname, hashed_password=pwd, is_active=True, is_superuser=is_super)
            db.add(u)
            users[role_name] = u
        await db.flush()
        
        # Assign roles
        for role_name, user in users.items():
            ur = UserRole(user_id=user.id, role_id=roles[role_name].id)
            db.add(ur)
        await db.flush()
        
        print("Seeding trials...")
        trials = []
        trials_data = [
            {
                "title": "Efficacy of Ashwagandha (Withania somnifera) in the Management of Osteoarthritis of Knee",
                "short_title": "AYU-OA-2024",
                "protocol_number": "AIIA/CT/2024/001",
                "registration_number": "CTRI/2024/01/067890",
                "phase": "Phase 3",
                "study_type": "Interventional",
                "intervention_type": "Drug",
                "therapeutic_area": "Musculoskeletal Disorders",
                "ayurveda_system": "Rasayana Chikitsa",
                "primary_objective": "To evaluate the efficacy and safety of Ashwagandha churna in reducing pain and improving joint function in patients with knee osteoarthritis compared to standard treatment.",
                "secondary_objectives": "Assessment of inflammatory markers, quality of life improvement, reduction in NSAID use",
                "inclusion_criteria": "Age 40-70 years, confirmed OA of knee (ACR criteria), pain VAS >= 40mm, willing to provide consent",
                "exclusion_criteria": "Severe OA requiring surgery, inflammatory arthritis, pregnancy, severe comorbidities",
                "planned_sample_size": 120,
                "sponsor": "All India Institute of Ayurveda, New Delhi",
                "start_date": date(2024, 3, 1),
                "expected_end_date": date(2025, 8, 31),
                "status": "RECRUITING",
            },
            {
                "title": "Ayurveda Multimodal Intervention for Type 2 Diabetes Mellitus: A Randomized Controlled Trial",
                "short_title": "AYU-DM-2024",
                "protocol_number": "AIIA/CT/2024/002",
                "registration_number": "CTRI/2024/03/068123",
                "phase": "Phase 2",
                "study_type": "Interventional",
                "intervention_type": "Drug + Lifestyle",
                "therapeutic_area": "Metabolic Disorders",
                "ayurveda_system": "Prameha Chikitsa",
                "primary_objective": "To assess the effect of a standardized Ayurveda multimodal intervention (herbal formulation + Yoga + Ahara-Vihara) on glycemic control in type 2 diabetes patients.",
                "secondary_objectives": "HbA1c reduction, lipid profile improvement, quality of life assessment",
                "inclusion_criteria": "Age 30-65 years, diagnosed T2DM (HbA1c 7-10%), on stable medication for 3 months",
                "exclusion_criteria": "Type 1 DM, insulin-dependent, renal impairment (eGFR < 60), pregnancy",
                "planned_sample_size": 90,
                "sponsor": "AIIA & Ministry of AYUSH",
                "start_date": date(2024, 6, 1),
                "expected_end_date": date(2025, 12, 31),
                "status": "ACTIVE",
            },
            {
                "title": "Clinical Evaluation of Brahmi-Ashwagandha Combination for Stress-Related Sleep Disorders",
                "short_title": "AYU-SLEEP-2024",
                "protocol_number": "AIIA/CT/2024/003",
                "registration_number": "",
                "phase": "Phase 2",
                "study_type": "Interventional",
                "intervention_type": "Drug",
                "therapeutic_area": "Neuropsychiatry",
                "ayurveda_system": "Medhya Rasayana",
                "primary_objective": "To evaluate the efficacy and safety of Brahmi-Ashwagandha formulation in improving sleep quality and reducing perceived stress in adults with stress-related insomnia.",
                "secondary_objectives": "PSS score reduction, PSQI improvement, cortisol level changes, safety assessment",
                "inclusion_criteria": "Age 25-55 years, PSQI > 5, PSS > 20, sleep complaints for >= 3 months",
                "exclusion_criteria": "Primary sleep disorders (OSA, RLS), psychiatric disorders, shift workers, pregnancy",
                "planned_sample_size": 60,
                "sponsor": "AIIA",
                "start_date": date(2024, 9, 1),
                "expected_end_date": date(2025, 6, 30),
                "status": "ETHICS_PENDING",
            },
        ]
        
        for td in trials_data:
            t = Trial(**td, pi_id=users["PRINCIPAL_INVESTIGATOR"].id)
            db.add(t)
            trials.append(t)
        await db.flush()
        
        # Study arms
        print("Seeding study arms...")
        arms = {}
        for i, t in enumerate(trials):
            if i == 0:
                a1 = StudyArm(trial_id=t.id, name="Ashwagandha Churna 500mg BD", description="Treatment arm - Ashwagandha churna 500mg twice daily", allocation_ratio=1.0, arm_type="TREATMENT")
                a2 = StudyArm(trial_id=t.id, name="Standard Care", description="Control arm - Standard conservative management", allocation_ratio=1.0, arm_type="CONTROL")
                db.add_all([a1, a2])
                arms[t.id] = [a1, a2]
            elif i == 1:
                a1 = StudyArm(trial_id=t.id, name="Ayurveda Multimodal", description="Herbal formulation + Yoga + Diet", allocation_ratio=1.0, arm_type="TREATMENT")
                a2 = StudyArm(trial_id=t.id, name="Conventional Care", description="Standard antidiabetic medication only", allocation_ratio=1.0, arm_type="CONTROL")
                a3 = StudyArm(trial_id=t.id, name="Ayurveda + Conventional", description="Combined Ayurveda and conventional care", allocation_ratio=1.0, arm_type="TREATMENT")
                db.add_all([a1, a2, a3])
                arms[t.id] = [a1, a2, a3]
            else:
                a1 = StudyArm(trial_id=t.id, name="Brahmi-Ashwagandha", description="Brahmi-Ashwagandha combination 300mg", allocation_ratio=1.0, arm_type="TREATMENT")
                a2 = StudyArm(trial_id=t.id, name="Placebo", description="Matching placebo capsules", allocation_ratio=1.0, arm_type="PLACEBO")
                db.add_all([a1, a2])
                arms[t.id] = [a1, a2]
        await db.flush()
        
        # Interventions
        print("Seeding interventions...")
        interventions = [
            Intervention(trial_id=trials[0].id, name="Ashwagandha Churna", type="Drug", description="Standardized Withania somnifera root powder", dosage="500 mg twice daily", duration="12 weeks", formulation="Churna (powder)"),
            Intervention(trial_id=trials[1].id, name="Nisha Amalaki Churna", type="Drug", description="Turmeric and Amla combination", dosage="3g twice daily", duration="24 weeks", formulation="Churna"),
            Intervention(trial_id=trials[1].id, name="Yoga Protocol", type="Lifestyle", description="Standardized yoga protocol for diabetes", dosage="45 min daily", duration="24 weeks"),
            Intervention(trial_id=trials[2].id, name="Brahmi-Ashwagandha Capsule", type="Drug", description="Standardized combination capsule", dosage="300 mg at bedtime", duration="8 weeks", formulation="Capsule"),
        ]
        db.add_all(interventions)
        await db.flush()
        # Map trial → primary drug intervention (first Drug-type per trial) for demo causative drug data
        trial_primary_drug: dict = {}
        for iv in interventions:
            if iv.type == "Drug" and iv.trial_id not in trial_primary_drug:
                trial_primary_drug[iv.trial_id] = iv.id
        
        # Milestones
        print("Seeding milestones...")
        for t in trials:
            milestones = [
                TrialMilestone(trial_id=t.id, name="Protocol Finalization", planned_date=t.start_date - timedelta(days=60), actual_date=t.start_date - timedelta(days=55), status="COMPLETED"),
                TrialMilestone(trial_id=t.id, name="Ethics Approval", planned_date=t.start_date - timedelta(days=30), actual_date=t.start_date - timedelta(days=25) if t.status != "ETHICS_PENDING" else None, status="COMPLETED" if t.status != "ETHICS_PENDING" else "PENDING"),
                TrialMilestone(trial_id=t.id, name="CTRI Registration", planned_date=t.start_date - timedelta(days=15), status="COMPLETED" if t.registration_number else "PENDING"),
                TrialMilestone(trial_id=t.id, name="First Patient In", planned_date=t.start_date, status="COMPLETED" if t.status in ("RECRUITING", "ACTIVE") else "PENDING"),
                TrialMilestone(trial_id=t.id, name="Interim Safety Data Cut", planned_date=date.today() - timedelta(days=3), status="PENDING", notes="Overdue pending cross-site data reconciliation"),
                TrialMilestone(trial_id=t.id, name="50% Cohort Monitoring Audit", planned_date=date.today() + timedelta(days=4), status="PENDING", notes="Approaching deadline for quarterly monitoring"),
                TrialMilestone(trial_id=t.id, name="50% Enrollment", planned_date=t.start_date + timedelta(days=120), status="PENDING"),
                TrialMilestone(trial_id=t.id, name="Last Patient Out", planned_date=t.expected_end_date, status="PENDING"),
            ]
            db.add_all(milestones)
        await db.flush()
        
        # Sites
        print("Seeding sites...")
        sites_data = [
            ("AIIA Hospital, New Delhi", "All India Institute of Ayurveda", "New Delhi", "Delhi", "110076"),
            ("NIA Jaipur", "National Institute of Ayurveda", "Jaipur", "Rajasthan", "302002"),
            ("IPGT&RA Jamnagar", "Institute for Post Graduate Teaching & Research in Ayurveda", "Jamnagar", "Gujarat", "361008"),
            ("RRAP Chennai", "Regional Research Institute of Ayurveda & Panchakarma", "Chennai", "Tamil Nadu", "600106"),
            ("CCRAS Bengaluru", "Central Council for Research in Ayurvedic Sciences Regional Center", "Bengaluru", "Karnataka", "560034"),
        ]
        sites = []
        for name, inst, city, state, pin in sites_data:
            s = Site(name=name, institution=inst, city=city, state=state, country="India", pin_code=pin, status="ACTIVE", activation_date=date(2024, 1, 15), target_enrollment=30, email=f"ctms@{city.lower().replace(' ', '')}.aiia.gov.in")
            db.add(s)
            sites.append(s)
        await db.flush()
        
        # Investigators
        print("Seeding investigators...")
        inv_data = [
            ("Dr. Anil Gupta", "MD (Ayurveda), PhD", "Kayachikitsa", 15, True),
            ("Dr. Deepa Nair", "MD (Ayurveda)", "Dravyaguna", 10, True),
            ("Dr. Ravi Shankar", "MS (Shalya Tantra)", "Shalya Tantra", 12, True),
            ("Dr. Pooja Verma", "MD (Prasuti Tantra)", "Prasuti Tantra", 8, True),
            ("Dr. Sudhir Patil", "MD (Ayurveda)", "Rasayana & Vajikarana", 20, True),
        ]
        investigators = []
        for idx, (name, qual, spec, exp, gcp) in enumerate(inv_data):
            inv = Investigator(site_id=sites[idx].id, name=name, qualification=qual, specialization=spec, experience_years=exp, gcp_trained=gcp, gcp_certificate_date=date(2023, 6, 1))
            db.add(inv)
            investigators.append(inv)
        await db.flush()
        
        # Site assignments
        print("Seeding site assignments...")
        for t in trials[:2]:
            for s in sites:
                sa = SiteAssignment(trial_id=t.id, site_id=s.id, pi_id=users["PRINCIPAL_INVESTIGATOR"].id, status="ACTIVE", activation_date=t.start_date, target_enrollment=t.planned_sample_size // 5)
                db.add(sa)
        await db.flush()
        
        # Participants
        print("Seeding participants (100+)...")
        participants = []
        genders = ["Male", "Female"]
        statuses_flow = ["SCREENED", "ELIGIBLE", "CONSENTED", "ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED", "WITHDRAWN"]
        
        for trial_idx, t in enumerate(trials[:2]):
            count = 60 if trial_idx == 0 else 45
            for i in range(count):
                site = random.choice(sites)
                age = random.randint(35, 68)
                gender = random.choice(genders)
                days_ago = random.randint(10, 200)
                scr_date = date.today() - timedelta(days=days_ago)
                
                # Determine status based on time
                if days_ago > 150:
                    st = random.choice(["ACTIVE", "COMPLETED", "RANDOMIZED"])
                elif days_ago > 100:
                    st = random.choice(["ENROLLED", "RANDOMIZED", "ACTIVE"])
                elif days_ago > 50:
                    st = random.choice(["CONSENTED", "ENROLLED", "RANDOMIZED"])
                else:
                    st = random.choice(["SCREENED", "ELIGIBLE", "CONSENTED"])
                
                if random.random() < 0.05:
                    st = "WITHDRAWN"
                
                enr_date = scr_date + timedelta(days=random.randint(3, 14)) if st in ("ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED") else None
                
                p = Participant(
                    participant_id=f"AIIA-{trial_idx+1}-{rand_id()}",
                    trial_id=t.id, site_id=site.id,
                    screening_date=scr_date, enrollment_date=enr_date,
                    status=st, age=age, gender=gender,
                )
                db.add(p)
                participants.append(p)
        await db.flush()
        
        # Consents for consented+ participants
        print("Seeding consents...")
        for p in participants:
            if p.status in ("CONSENTED", "ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED"):
                c = Consent(participant_id=p.id, consent_date=p.screening_date + timedelta(days=random.randint(1, 5)), consent_version="1.0", consented_by=users["STUDY_COORDINATOR"].id, witness_name="Study Witness")
                db.add(c)
        await db.flush()
        
        # Enrollments
        print("Seeding enrollments...")
        for p in participants:
            if p.enrollment_date:
                e = Enrollment(participant_id=p.id, enrollment_date=p.enrollment_date, enrolled_by=users["STUDY_COORDINATOR"].id, enrollment_number=f"ENR-{rand_id()}")
                db.add(e)
        await db.flush()
        
        # Randomizations
        print("Seeding randomizations...")
        for p in participants:
            if p.status in ("RANDOMIZED", "ACTIVE", "COMPLETED"):
                trial_arms = arms.get(p.trial_id, [])
                if trial_arms:
                    arm = random.choice(trial_arms)
                    r = Randomization(participant_id=p.id, trial_id=p.trial_id, randomization_date=p.enrollment_date + timedelta(days=1) if p.enrollment_date else date.today(), randomization_number=f"R-{rand_id()}", assigned_arm_id=arm.id, assigned_arm_name=arm.name, randomized_by=users["STUDY_COORDINATOR"].id, is_locked=True)
                    db.add(r)
        await db.flush()
        
        # Visit definitions
        print("Seeding visit definitions...")
        visit_defs = {}
        for t in trials[:2]:
            vds = [
                VisitDefinition(trial_id=t.id, visit_name="Screening", visit_number=0, visit_type="SCREENING", day_offset=-7, is_required=True),
                VisitDefinition(trial_id=t.id, visit_name="Baseline", visit_number=1, visit_type="BASELINE", day_offset=0, is_required=True),
                VisitDefinition(trial_id=t.id, visit_name="Week 2", visit_number=2, visit_type="TREATMENT", day_offset=14, is_required=True),
                VisitDefinition(trial_id=t.id, visit_name="Week 4", visit_number=3, visit_type="TREATMENT", day_offset=28, is_required=True),
                VisitDefinition(trial_id=t.id, visit_name="Week 8", visit_number=4, visit_type="TREATMENT", day_offset=56, is_required=True),
                VisitDefinition(trial_id=t.id, visit_name="Week 12", visit_number=5, visit_type="TREATMENT", day_offset=84, is_required=True),
                VisitDefinition(trial_id=t.id, visit_name="End of Study", visit_number=6, visit_type="END_OF_STUDY", day_offset=90, is_required=True),
            ]
            db.add_all(vds)
            visit_defs[t.id] = vds
        await db.flush()
        
        # Participant visits
        print("Seeding participant visits...")
        for p in participants:
            if p.status in ("ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED") and p.enrollment_date:
                vds = visit_defs.get(p.trial_id, [])
                for vd in vds:
                    sched_date = p.enrollment_date + timedelta(days=vd.day_offset)
                    if sched_date > date.today():
                        st = "SCHEDULED"
                        actual = None
                    elif random.random() < 0.85:
                        st = "COMPLETED"
                        actual = sched_date + timedelta(days=random.randint(-2, 3))
                    elif random.random() < 0.5:
                        st = "OVERDUE"
                        actual = None
                    else:
                        st = "MISSED"
                        actual = None
                    
                    pv = ParticipantVisit(participant_id=p.id, visit_definition_id=vd.id, visit_name=vd.visit_name, scheduled_date=sched_date, actual_date=actual, status=st, completed_by=users["STUDY_COORDINATOR"].id if st == "COMPLETED" else None)
                    db.add(pv)

        # Explicit demo overdue visits across multiple trials/participants
        active_parts = [p for p in participants if p.status in ("ENROLLED", "RANDOMIZED", "ACTIVE")]
        if len(active_parts) >= 3:
            explicit_overdue_visits = [
                {
                    "part": active_parts[0],
                    "vname": "Week 4 Clinical & Lab Assessment",
                    "days_ago": 5,
                    "status": "OVERDUE",
                },
                {
                    "part": active_parts[1],
                    "vname": "Week 8 Vital Signs & Fasting Glucose",
                    "days_ago": 3,
                    "status": "SCHEDULED",
                },
                {
                    "part": active_parts[2],
                    "vname": "Week 12 Efficacy & Biomarker Endpoint",
                    "days_ago": 2,
                    "status": "OVERDUE",
                },
            ]
            for ov in explicit_overdue_visits:
                db.add(ParticipantVisit(
                    participant_id=ov["part"].id,
                    visit_definition_id=visit_defs.get(ov["part"].trial_id, [None])[0].id if visit_defs.get(ov["part"].trial_id) else None,
                    visit_name=ov["vname"],
                    scheduled_date=date.today() - timedelta(days=ov["days_ago"]),
                    actual_date=None,
                    status=ov["status"],
                    notes="Flagged for coordinator phone follow-up",
                ))

        await db.flush()
        
        # Forms
        print("Seeding forms...")
        form_defs = []
        for t in trials[:2]:
            f1 = Form(trial_id=t.id, name="Demographics", code="DM", description="Participant demographics", version="1.0", status="ACTIVE", visit_type="SCREENING")
            f2 = Form(trial_id=t.id, name="Vital Signs", code="VS", description="Vital signs assessment", version="1.0", status="ACTIVE", visit_type="TREATMENT")
            f3 = Form(trial_id=t.id, name="Primary Efficacy", code="EFF", description="Primary efficacy outcome measures", version="1.0", status="ACTIVE", visit_type="TREATMENT")
            db.add_all([f1, f2, f3])
            form_defs.extend([f1, f2, f3])
        await db.flush()
        
        # Form fields
        print("Seeding form fields...")
        for f in form_defs:
            if f.code == "DM":
                fields = [
                    FormField(form_id=f.id, field_name="age", field_label="Age (years)", field_type="NUMBER", is_required=True, validation_rules={"min": 18, "max": 120}, order_index=1, cdisc_domain="DM", cdisc_variable="AGE", unit="years"),
                    FormField(form_id=f.id, field_name="gender", field_label="Gender", field_type="SINGLE_SELECT", is_required=True, options=["Male", "Female", "Other"], order_index=2, cdisc_domain="DM", cdisc_variable="SEX"),
                    FormField(form_id=f.id, field_name="occupation", field_label="Occupation", field_type="TEXT", order_index=3),
                    FormField(form_id=f.id, field_name="prakriti", field_label="Prakriti (Constitution)", field_type="SINGLE_SELECT", options=["Vata", "Pitta", "Kapha", "Vata-Pitta", "Pitta-Kapha", "Vata-Kapha", "Sama"], order_index=4),
                ]
            elif f.code == "VS":
                fields = [
                    FormField(form_id=f.id, field_name="systolic_bp", field_label="Systolic BP", field_type="NUMBER", is_required=True, validation_rules={"min": 60, "max": 250}, order_index=1, unit="mmHg"),
                    FormField(form_id=f.id, field_name="diastolic_bp", field_label="Diastolic BP", field_type="NUMBER", is_required=True, validation_rules={"min": 40, "max": 150}, order_index=2, unit="mmHg"),
                    FormField(form_id=f.id, field_name="heart_rate", field_label="Heart Rate", field_type="NUMBER", is_required=True, validation_rules={"min": 40, "max": 200}, order_index=3, unit="bpm"),
                    FormField(form_id=f.id, field_name="temperature", field_label="Body Temperature", field_type="NUMBER", validation_rules={"min": 35.0, "max": 42.0}, order_index=4, unit="\u00b0C"),
                    FormField(form_id=f.id, field_name="weight", field_label="Body Weight", field_type="NUMBER", validation_rules={"min": 20, "max": 200}, order_index=5, unit="kg"),
                ]
            else:
                fields = [
                    FormField(form_id=f.id, field_name="pain_vas", field_label="Pain VAS Score", field_type="NUMBER", is_required=True, validation_rules={"min": 0, "max": 100}, order_index=1, unit="mm"),
                    FormField(form_id=f.id, field_name="womac_score", field_label="WOMAC Score", field_type="NUMBER", validation_rules={"min": 0, "max": 96}, order_index=2),
                    FormField(form_id=f.id, field_name="global_assessment", field_label="Patient Global Assessment", field_type="SINGLE_SELECT", options=["Much Better", "Better", "No Change", "Worse", "Much Worse"], order_index=3),
                    FormField(form_id=f.id, field_name="comments", field_label="Clinical Comments", field_type="TEXT", order_index=4),
                ]
            db.add_all(fields)
        await db.flush()
        
        # Form submissions (sample)
        print("Seeding form submissions...")
        submitted_count = 0
        for p in participants[:40]:
            for f in form_defs[:2]:
                if f.trial_id == p.trial_id:
                    data = {}
                    if f.code == "VS":
                        data = {"systolic_bp": str(random.randint(110, 150)), "diastolic_bp": str(random.randint(70, 95)), "heart_rate": str(random.randint(60, 90)), "temperature": str(round(random.uniform(36.0, 37.2), 1)), "weight": str(round(random.uniform(50, 90), 1))}
                    elif f.code == "DM":
                        data = {"age": str(p.age), "gender": p.gender, "occupation": random.choice(["Teacher", "Farmer", "Business", "Homemaker", "IT Professional"])}
                    sub = FormSubmission(form_id=f.id, participant_id=p.id, submitted_by=users["STUDY_COORDINATOR"].id, submitted_at=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 100)), status="SUBMITTED", data=data)
                    db.add(sub)
                    submitted_count += 1
        await db.flush()
        
        # Data queries
        print("Seeding data queries...")
        # Get the first few submissions to link queries to
        from sqlalchemy import select as sel
        subs_result = await db.execute(sel(FormSubmission).limit(3))
        subs_list = subs_result.scalars().all()
        if len(subs_list) >= 3:
            dqs = [
                DataQuery(submission_id=subs_list[0].id, query_text="Blood pressure reading seems high - please verify", query_type="MANUAL", status="OPEN", raised_by=users["DATA_MANAGER"].id),
                DataQuery(submission_id=subs_list[1].id, query_text="Missing weight measurement", query_type="AUTO_VALIDATION", status="OPEN", raised_by=users["DATA_MANAGER"].id),
                DataQuery(submission_id=subs_list[2].id, query_text="VAS score exceeds expected range", query_type="MANUAL", status="ANSWERED", raised_by=users["DATA_MANAGER"].id, answer_text="Score verified by PI"),
            ]
            db.add_all(dqs)
        await db.flush()
        
        # Ethics committees
        print("Seeding ethics committees...")
        ec1 = EthicsCommittee(name="AIIA Institutional Ethics Committee", institution="All India Institute of Ayurveda", registration_number="ECR/1382/Inst/DL/2020", chairperson="Prof. Tanuja Nesari", contact_email="iec@aiia.gov.in")
        ec2 = EthicsCommittee(name="NIA Ethics Committee", institution="National Institute of Ayurveda", registration_number="ECR/456/Inst/RJ/2019", chairperson="Prof. Sanjeev Sharma", contact_email="iec@nia.nic.in")
        db.add_all([ec1, ec2])
        await db.flush()
        
        # Ethics submissions
        print("Seeding ethics submissions...")
        ethics_subs = []
        for t in trials:
            es = EthicsSubmission(trial_id=t.id, committee_id=ec1.id, submission_type="INITIAL", submission_date=t.start_date - timedelta(days=45), status="APPROVED" if t.status != "ETHICS_PENDING" else "UNDER_REVIEW", submitted_by=users["PRINCIPAL_INVESTIGATOR"].id, title=f"Ethics review for {t.short_title}", description=f"Initial ethics submission for {t.title}")
            db.add(es)
            ethics_subs.append(es)
        await db.flush()
        
        # Ethics approvals
        print("Seeding ethics approvals...")
        for i, es in enumerate(ethics_subs):
            if trials[i].status != "ETHICS_PENDING":
                ea = EthicsApproval(submission_id=es.id, trial_id=trials[i].id, approval_number=f"IEC/AIIA/2024/{i+1:03d}", approval_date=trials[i].start_date - timedelta(days=20), valid_from=trials[i].start_date - timedelta(days=20), valid_until=trials[i].start_date + timedelta(days=345))
                db.add(ea)
        await db.flush()
        
        # Ethics reviews
        for es in ethics_subs:
            er = EthicsReview(submission_id=es.id, reviewer="Prof. Tanuja Nesari", review_date=es.submission_date + timedelta(days=14) if es.submission_date else date.today(), decision="APPROVED" if es.status == "APPROVED" else "UNDER_REVIEW", comments="Protocol reviewed and found satisfactory" if es.status == "APPROVED" else "Review in progress")
            db.add(er)
        await db.flush()
        
        # Regulatory records
        print("Seeding regulatory records...")
        for t in trials:
            rr = RegulatoryRecord(trial_id=t.id, record_type="CTRI", registration_number=t.registration_number or None, submission_date=t.start_date - timedelta(days=30) if t.registration_number else None, registration_date=t.start_date - timedelta(days=15) if t.registration_number else None, status="REGISTERED" if t.registration_number else "NOT_STARTED", responsible_officer_id=users["REGULATORY_OFFICER"].id, notes="CTRI registration tracking")
            db.add(rr)
        await db.flush()
        
        # NDCT Checklists
        print("Seeding NDCT checklists...")
        ndct_items = [
            "Investigator qualification and GCP training documented",
            "Ethics committee approval obtained",
            "CTRI registration completed",
            "Informed consent form approved and versioned",
            "Insurance/compensation provision arranged",
            "Serious Adverse Event reporting procedure established",
            "Data Safety Monitoring Board constituted",
            "Study drug quality testing completed",
            "Site initiation visits completed",
            "Source data verification procedures documented",
        ]
        for t in trials[:2]:
            for i, item in enumerate(ndct_items):
                cl = RegulatoryChecklist(trial_id=t.id, category="NDCT_RULES_2019", item_name=item, description=f"NDCT Rules 2019 compliance item: {item}", is_completed=i < 6, completed_date=date.today() - timedelta(days=random.randint(10, 90)) if i < 6 else None, completed_by=users["REGULATORY_OFFICER"].id if i < 6 else None)
                db.add(cl)
        await db.flush()
        
        # Adverse Events
        print("Seeding adverse events...")
        ae_terms = [
            ("Headache", "MILD", "NON_SERIOUS", "UNLIKELY", "RECOVERED"),
            ("Nausea", "MILD", "NON_SERIOUS", "POSSIBLE", "RECOVERED"),
            ("Gastric discomfort", "MILD", "NON_SERIOUS", "POSSIBLE", "RECOVERED"),
            ("Dizziness", "MODERATE", "NON_SERIOUS", "POSSIBLE", "RECOVERING"),
            ("Skin rash", "MODERATE", "NON_SERIOUS", "PROBABLE", "RECOVERED"),
            ("Joint pain exacerbation", "MODERATE", "NON_SERIOUS", "UNLIKELY", "RECOVERED"),
            ("Diarrhea", "MILD", "NON_SERIOUS", "POSSIBLE", "RECOVERED"),
            ("Insomnia", "MILD", "NON_SERIOUS", "UNLIKELY", "RECOVERED"),
            ("Elevated liver enzymes", "MODERATE", "NON_SERIOUS", "POSSIBLE", "RECOVERING"),
            ("Upper respiratory infection", "MILD", "NON_SERIOUS", "UNRELATED", "RECOVERED"),
            ("Fatigue", "MILD", "NON_SERIOUS", "POSSIBLE", "RECOVERED"),
            ("Back pain", "MODERATE", "NON_SERIOUS", "UNRELATED", "RECOVERED"),
            ("Hypoglycemia episode", "MODERATE", "NON_SERIOUS", "POSSIBLE", "RECOVERED"),
            ("Abdominal pain", "MODERATE", "NON_SERIOUS", "POSSIBLE", "RECOVERED"),
            ("Constipation", "MILD", "NON_SERIOUS", "UNLIKELY", "RECOVERED"),
            ("Allergic reaction", "MODERATE", "NON_SERIOUS", "PROBABLE", "RECOVERED"),
            ("Hypertensive episode", "SEVERE", "SERIOUS", "POSSIBLE", "RECOVERED"),
            ("Chest pain", "SEVERE", "SERIOUS", "UNRELATED", "RECOVERED"),
            ("Hospitalization - pneumonia", "SEVERE", "SERIOUS", "UNRELATED", "RECOVERING"),
            ("Severe allergic reaction", "SEVERE", "SERIOUS", "PROBABLE", "RECOVERED"),
            ("Syncope", "MODERATE", "SERIOUS", "POSSIBLE", "RECOVERED"),
        ]
        
        aes = []
        for p in random.sample(participants, min(len(participants), 25)):
            ae_data = random.choice(ae_terms)
            ae = AdverseEvent(
                participant_id=p.id, trial_id=p.trial_id, site_id=p.site_id,
                event_term=ae_data[0], description=f"Patient reported {ae_data[0].lower()} during treatment period",
                onset_date=date.today() - timedelta(days=random.randint(5, 150)),
                resolution_date=date.today() - timedelta(days=random.randint(0, 5)) if ae_data[4] == "RECOVERED" else None,
                severity=ae_data[1], seriousness=ae_data[2], causality=ae_data[3],
                expectedness="EXPECTED" if ae_data[3] in ("UNLIKELY", "UNRELATED") else "UNEXPECTED",
                action_taken="Dose maintained" if ae_data[1] == "MILD" else "Dose modified",
                outcome=ae_data[4], reporter_id=users["PRINCIPAL_INVESTIGATOR"].id,
                reported_date=date.today() - timedelta(days=random.randint(3, 145)),
                status="REPORTED",
                suspected_causative_drug_id=trial_primary_drug.get(p.trial_id) if ae_data[3] in ("POSSIBLE", "PROBABLE", "DEFINITE") else None,
            )
            db.add(ae)
            aes.append(ae)

        # Explicit demo Adverse Events exceeding the 5-day review window
        demo_pending_aes = [
            {
                "term": "Persistent joint swelling and localized erythema",
                "desc": "Participant reported persistent effusion and swelling in right knee joint post-treatment session.",
                "days_ago": 9,
                "sev": "MODERATE",
                "ser": "NON_SERIOUS",
                "caus": "POSSIBLE",
                "trial": trials[0],
                "site": sites[0],
            },
            {
                "term": "Recurrent abdominal cramping post-dose",
                "desc": "Recurrent mild to moderate epigastric pain and cramping reported 30 mins after taking evening dose.",
                "days_ago": 7,
                "sev": "MODERATE",
                "ser": "NON_SERIOUS",
                "caus": "PROBABLE",
                "trial": trials[1],
                "site": sites[1],
            },
            {
                "term": "Mild dizziness and headache",
                "desc": "Episodes of lightheadedness and frontal headache observed during morning ambulatory monitoring.",
                "days_ago": 6,
                "sev": "MILD",
                "ser": "NON_SERIOUS",
                "caus": "POSSIBLE",
                "trial": trials[0],
                "site": sites[2],
            },
        ]
        for item in demo_pending_aes:
            # Pick a participant matching trial or first available
            matching_part = next((pt for pt in participants if pt.trial_id == item["trial"].id), participants[0])
            ae_explicit = AdverseEvent(
                participant_id=matching_part.id,
                trial_id=item["trial"].id,
                site_id=item["site"].id,
                event_term=item["term"],
                description=item["desc"],
                onset_date=date.today() - timedelta(days=item["days_ago"] + 2),
                resolution_date=None,
                severity=item["sev"],
                seriousness=item["ser"],
                causality=item["caus"],
                expectedness="UNEXPECTED",
                action_taken="Pending PI Clinical Evaluation",
                outcome="NOT_RECOVERED",
                reporter_id=users["PRINCIPAL_INVESTIGATOR"].id,
                reported_date=date.today() - timedelta(days=item["days_ago"]),
                status="REPORTED",
                suspected_causative_drug_id=trial_primary_drug.get(item["trial"].id),
            )
            db.add(ae_explicit)
            aes.append(ae_explicit)

        await db.flush()
        
        # SAEs
        print("Seeding SAEs...")
        serious_aes = [ae for ae in aes if ae.seriousness == "SERIOUS"]
        for ae in serious_aes:
            sae = SeriousAdverseEvent(
                adverse_event_id=ae.id, sae_number=f"SAE-{rand_id()}",
                criteria="HOSPITALIZATION" if "Hospitalization" in ae.event_term else "LIFE_THREATENING" if ae.severity == "SEVERE" else "OTHER",
                narrative=f"Patient experienced {ae.event_term}. Immediate medical attention provided. Patient managed with standard care.",
                reported_to_sponsor_date=ae.reported_date + timedelta(days=1) if ae.reported_date else date.today(),
                reported_to_ethics_date=ae.reported_date + timedelta(days=3) if ae.reported_date else None,
                status=random.choice(["REPORTED", "UNDER_REVIEW", "MEDICAL_REVIEW"]),
            )
            db.add(sae)
        await db.flush()
        
        # Causality assessments
        print("Seeding causality assessments...")
        for ae in aes[:10]:
            ca = CausalityAssessment(adverse_event_id=ae.id, assessor_id=users["PHARMACOVIGILANCE_OFFICER"].id, assessment_date=ae.reported_date + timedelta(days=5) if ae.reported_date else date.today(), method="WHO-UMC", causality_rating=ae.causality, rationale=f"Assessed using WHO-UMC criteria. Temporal relationship and biological plausibility considered.")
            db.add(ca)
        await db.flush()
        
        # Safety signals
        print("Seeding safety signals...")
        ss = SafetySignal(trial_id=trials[0].id, signal_term="Elevated liver enzymes cluster", description="Three participants showed elevated ALT/AST levels above 2x ULN in treatment arm", detected_date=date.today() - timedelta(days=30), status="UNDER_REVIEW", severity="MODERATE", action_taken="Increased liver function monitoring frequency")
        db.add(ss)
        await db.flush()
        
        # Documents
        print("Seeding documents...")
        doc_types = [
            ("Protocol v1.0 - AYU-OA-2024", "PROTOCOL"),
            ("Informed Consent Form v1.0", "CONSENT_FORM"),
            ("IEC Approval Letter", "ETHICS_APPROVAL"),
            ("CTRI Registration Certificate", "REGULATORY"),
            ("Investigator Brochure - Ashwagandha", "INVESTIGATOR_BROCHURE"),
            ("Annual Safety Report 2024", "SAFETY_REPORT"),
            ("GCP Training Certificate - Dr. Gupta", "OTHER"),
            ("Protocol v1.0 - AYU-DM-2024", "PROTOCOL"),
            ("Site Initiation Report - AIIA Delhi", "OTHER"),
            ("Data Management Plan v1.0", "OTHER"),
        ]
        for title, dtype in doc_types:
            d = Document(trial_id=trials[0].id if "OA" in title else trials[1].id if "DM" in title else None, title=title, document_type=dtype, file_name=f"{title.replace(' ', '_').lower()}.pdf", uploaded_by=users["TRIAL_ADMIN"].id, version="1.0", status="ACTIVE", description=f"Document: {title}")
            db.add(d)
        await db.flush()
        
        # CDISC Mappings
        print("Seeding CDISC mappings...")
        cdisc_maps = [
            ("Participant", "participant_id", "DM", "USUBJID", "Direct mapping"),
            ("Participant", "age", "DM", "AGE", "Direct mapping"),
            ("Participant", "gender", "DM", "SEX", "First letter uppercase"),
            ("Participant", "enrollment_date", "DM", "RFSTDTC", "ISO 8601 format"),
            ("ParticipantVisit", "visit_name", "SV", "VISIT", "Direct mapping"),
            ("ParticipantVisit", "actual_date", "SV", "SVSTDTC", "ISO 8601 format"),
            ("AdverseEvent", "event_term", "AE", "AETERM", "Direct mapping"),
            ("AdverseEvent", "severity", "AE", "AESEV", "Direct mapping"),
            ("AdverseEvent", "seriousness", "AE", "AESER", "Y/N mapping"),
            ("AdverseEvent", "causality", "AE", "AEREL", "Direct mapping"),
            ("AdverseEvent", "onset_date", "AE", "AESTDTC", "ISO 8601 format"),
            ("AdverseEvent", "resolution_date", "AE", "AEENDTC", "ISO 8601 format"),
            ("AdverseEvent", "outcome", "AE", "AEOUT", "Coded mapping"),
        ]
        for entity, field, domain, var, rule in cdisc_maps:
            cm = CDISCMapping(internal_entity=entity, internal_field=field, cdisc_domain=domain, cdisc_variable=var, transformation_rule=rule, is_active=True)
            db.add(cm)
        await db.flush()
        
        # Audit logs
        print("Seeding audit logs...")
        audit_actions = [
            ("CREATE", "Trial", "Trial AYU-OA-2024 created", users["TRIAL_ADMIN"]),
            ("CREATE", "Trial", "Trial AYU-DM-2024 created", users["TRIAL_ADMIN"]),
            ("CREATE", "Site", "AIIA Hospital site added", users["TRIAL_ADMIN"]),
            ("UPDATE", "Trial", "Trial status changed to RECRUITING", users["TRIAL_ADMIN"]),
            ("CREATE", "Participant", "New participant screened", users["STUDY_COORDINATOR"]),
            ("UPDATE", "Participant", "Participant consented", users["STUDY_COORDINATOR"]),
            ("UPDATE", "Participant", "Participant enrolled", users["STUDY_COORDINATOR"]),
            ("UPDATE", "Participant", "Participant randomized", users["STUDY_COORDINATOR"]),
            ("CREATE", "FormSubmission", "Vital signs eCRF submitted", users["STUDY_COORDINATOR"]),
            ("CREATE", "AdverseEvent", "Adverse event reported: Headache", users["PRINCIPAL_INVESTIGATOR"]),
            ("CREATE", "SeriousAdverseEvent", "SAE reported: Hypertensive episode", users["PRINCIPAL_INVESTIGATOR"]),
            ("CREATE", "EthicsSubmission", "Ethics submission created", users["PRINCIPAL_INVESTIGATOR"]),
            ("UPDATE", "EthicsSubmission", "Ethics approval granted", users["ETHICS_COMMITTEE"]),
            ("CREATE", "RegulatoryRecord", "CTRI registration initiated", users["REGULATORY_OFFICER"]),
            ("UPDATE", "RegulatoryRecord", "CTRI registration completed", users["REGULATORY_OFFICER"]),
            ("CREATE", "Document", "Protocol document uploaded", users["TRIAL_ADMIN"]),
            ("LOGIN", "User", "User logged in", users["SUPER_ADMIN"]),
            ("CREATE", "DataQuery", "Data query raised for BP reading", users["DATA_MANAGER"]),
            ("UPDATE", "Visit", "Visit completed", users["STUDY_COORDINATOR"]),
            ("EXPORT", "CDISC", "SDTM export generated for trial", users["DATA_MANAGER"]),
        ]
        for i, (action, entity, details, user) in enumerate(audit_actions):
            al = AuditLog(
                timestamp=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 180), hours=random.randint(0, 23)),
                user_id=user.id, user_email=user.email,
                user_role=getattr(user, "username", "user"),
                action=action, entity_type=entity,
                details=details,
            )
            db.add(al)
        await db.flush()
        
        # Notifications
        print("Seeding notifications...")
        notif_data = [
            (users["PRINCIPAL_INVESTIGATOR"], "SAE Reported", "A serious adverse event has been reported for participant AIIA-1-xxxxx", "SAE_REPORTED", "HIGH"),
            (users["PRINCIPAL_INVESTIGATOR"], "Overdue Visit", "Participant AIIA-1-xxxxx has an overdue visit (Week 4)", "OVERDUE_VISIT", "NORMAL"),
            (users["ETHICS_COMMITTEE"], "Ethics Renewal Due", "Ethics approval for AYU-OA-2024 expires in 30 days", "ETHICS_EXPIRING", "HIGH"),
            (users["REGULATORY_OFFICER"], "Regulatory Deadline", "CTRI annual update due for AYU-DM-2024", "REGULATORY_DEADLINE", "NORMAL"),
            (users["DATA_MANAGER"], "Data Query Created", "New data query raised for participant vitals", "DATA_QUERY", "NORMAL"),
            (users["STUDY_COORDINATOR"], "New Enrollment", "Participant successfully enrolled in AYU-OA-2024", "SYSTEM", "LOW"),
            (users["SUPER_ADMIN"], "System Update", "AIIA CTMS has been updated to version 1.0", "SYSTEM", "LOW"),
            (users["SUPER_ADMIN"], "Demo Trial Milestone", "Trial AYU-OA-2024 has enrolled 85/120 participants (70.8% target reached)", "SYSTEM", "HIGH"),
            (users["SUPER_ADMIN"], "Demo Ethics Approval", "Central Ethics Committee approved Protocol Amendment v2.1 for AYU-OA-2024", "SYSTEM", "NORMAL"),
            (users["SUPER_ADMIN"], "Demo DSMB Interim Sign-off", "DSMB interim efficacy and safety review is ready for administrative sign-off", "SYSTEM", "HIGH"),
            (users["SUPER_ADMIN"], "Demo CDISC Export Ready", "SDTM validation package for AYU-OA-2024 generated with zero fatal schema errors", "SYSTEM", "NORMAL"),
        ]
        for user, title, msg, ntype, priority in notif_data:
            n = Notification(user_id=user.id, title=title, message=msg, type=ntype, priority=priority)
            db.add(n)
        await db.flush()
        
        await db.commit()
        print(f"\nSeed data created successfully!")
        print(f"  - {len(users_data)} users")
        print(f"  - {len(trials_data)} trials")
        print(f"  - {len(sites_data)} sites")
        print(f"  - {len(participants)} participants")
        print(f"  - {len(aes)} adverse events")
        print(f"  - {len(serious_aes)} SAEs")
        print(f"  - {submitted_count} form submissions")
        print(f"  - {len(cdisc_maps)} CDISC mappings")
        print(f"  - {len(audit_actions)} audit logs")
        print(f"  - {len(notif_data)} notifications")

if __name__ == "__main__":
    asyncio.run(seed_data())
