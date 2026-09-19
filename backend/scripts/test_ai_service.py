"""
Quick end-to-end smoke test for the Claude wrapper.

Usage (from backend/):
    python scripts/test_ai_service.py

Requires ANTHROPIC_API_KEY set in .env or the environment.
"""
import asyncio
import sys
import os

# Allow running from repo root or backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.ai_service import ask_claude


async def main():
    print("Calling Claude…")
    try:
        reply = await ask_claude("Say hello in one sentence.")
        print("Claude says:", reply)
    except RuntimeError as exc:
        print("ERROR:", exc)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
