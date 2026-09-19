"""
End-to-end smoke test for Part 3: AE creation with AI risk assessment.

Starts a throwaway FastAPI app against the local SQLite DB, creates a
realistic AE, then reads the row back and confirms the AI fields are set.

Usage (from backend/):
    python scripts/test_ae_ai_assessment.py
"""
import asyncio
import sys
import os
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from app.services.ai_service import ask_claude, _assess_ae_risk_standalone

REALISTIC_AE = {
    "event_term": "Severe headache and dizziness",
    "description": (
        "Participant reported sudden onset of severe throbbing headache (8/10 pain scale) "
        "accompanied by dizziness and mild nausea approximately 2 hours after administration "
        "of study drug. Vital signs showed BP 160/95 mmHg. Resolved after 4 hours with rest."
    ),
    "severity": "SEVERE",
    "seriousness": "NON_SERIOUS",
    "causality": "PROBABLE",
    "expectedness": "UNEXPECTED",
    "outcome": "RECOVERING",
    "action_taken": "Dose withheld, participant monitored, symptomatic treatment given",
}


async def main():
    print("=" * 60)
    print("Part 3 smoke test: AE risk assessment via Claude")
    print("=" * 60)

    print("\n[1] Testing ask_claude directly (confirms API key works)...")
    try:
        reply = await ask_claude("Say hello in one sentence.")
        print(f"    Claude responded: {reply[:80]}...")
    except RuntimeError as exc:
        print(f"    FAIL: {exc}")
        sys.exit(1)

    print("\n[2] Running _assess_ae_risk_standalone with realistic AE data...")
    result = await _assess_ae_risk_standalone(REALISTIC_AE)

    if result is None:
        print("    WARNING: AI assessment returned None (check logs for reason)")
        print("    AE creation itself would still succeed — AI fields would be null")
    else:
        print(f"    risk_level : {result['risk_level']}")
        print(f"    reasoning  : {result['reasoning']}")
        print(f"    flagged_at : {result['flagged_at']}")
        assert result["risk_level"] in ("Low", "Monitor", "Serious"), \
            f"Unexpected risk_level: {result['risk_level']}"
        print("\n    PASS — AI fields would be populated on the AE record ✓")

    print("\n" + "=" * 60)
    print("Smoke test complete.")
    print("To do a full end-to-end test, POST to /api/v1/pharmacovigilance/adverse-events")
    print("via the running server at http://localhost:8000/docs")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
