"""
Minimal connectivity sanity check for Anthropic API.
Loads ANTHROPIC_API_KEY from app.core.config.settings (which reads .env via Pydantic).
Calls Anthropic API using model 'claude-sonnet-4-6'.
"""
import sys
import os

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings


def main():
    api_key = settings.ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY", "")
    
    if not api_key or "your-anthropic-api-key" in api_key:
        print("=" * 60)
        print("[!] ANTHROPIC_API_KEY is not set or is still a placeholder.")
        print("    Add your Anthropic key into .env:")
        print("    ANTHROPIC_API_KEY=sk-ant-api03-...")
        print("=" * 60)
        sys.exit(1)

    print(f"[*] Found ANTHROPIC_API_KEY: {api_key[:8]}...{api_key[-4:]}")
    print("[*] Sending test prompt to Anthropic API (model: claude-sonnet-4-6)...")

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Respond with: 'Anthropic connectivity check passed successfully! AIIA CTMS is ready.'"
                }
            ],
        )
        reply = "".join(b.text for b in response.content if hasattr(b, "text"))
        print("\n[SUCCESS] Response received from Claude:")
        print(reply)
        print("\nEnd-to-end connectivity check PASSED.")
    except Exception as exc:
        print(f"\n[ERROR] Anthropic API call failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
