#!/usr/bin/env python3
"""Independent copy/visual audit via Gemini on Vertex AI (relay-imagegen-33421)."""
import sys
from pathlib import Path
from google import genai
from google.genai import types

HERE = Path(__file__).parent
prompt = (HERE / "audit_prompt.txt").read_text(encoding="utf-8")
# inline the copy dump (replace @ref so the model definitely sees it)
copy = (HERE / "copy_dump.md").read_text(encoding="utf-8")
prompt = prompt.replace("@copy_dump.md", "\n\n=== КОПИЯ ===\n" + copy + "\n=== /КОПИЯ ===\n")

parts = [types.Part.from_text(text=prompt)]
for img in ["exp.jpeg", "roles.jpeg"]:
    p = HERE / img
    if p.exists():
        parts.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg"))

client = genai.Client(vertexai=True, project="relay-imagegen-33421", location="global")
for model in ("gemini-2.5-pro",):
    try:
        resp = client.models.generate_content(
            model=model,
            contents=[types.Content(role="user", parts=parts)],
            config=types.GenerateContentConfig(
                temperature=0.65,
                thinking_config=types.ThinkingConfig(thinking_budget=8000),
            ),
        )
        (HERE / "gemini_audit.md").write_text(resp.text or "(empty)", encoding="utf-8")
        sys.stderr.write(f"OK {model}: {len(resp.text or '')} chars\n")
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"[{model} failed: {e}]\n")
sys.exit(1)
