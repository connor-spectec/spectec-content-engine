#!/usr/bin/env python3
"""
SpecTec Content Pipeline
Runs the 5-step master content pipeline against the Anthropic API.
Usage: python pipeline.py
"""

import os
import sys
import glob
import datetime
import anthropic
from config import INPUTS, KNOWLEDGE_BASE_DIR, PROMPTS_DIR, SYSTEM_PROMPT_FILE, OUTPUT_DIR

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_knowledge_base() -> str:
    """Concatenate all knowledge base files into one context block."""
    files = sorted(glob.glob(os.path.join(KNOWLEDGE_BASE_DIR, "*")))
    sections = []
    for fp in files:
        if os.path.isfile(fp):
            filename = os.path.basename(fp)
            try:
                content = load_file(fp)
                sections.append(f"=== KNOWLEDGE BASE FILE: {filename} ===\n{content}\n")
            except Exception as e:
                print(f"  ⚠ Could not read {filename}: {e}")
    return "\n".join(sections)

def load_prompt(step_number: int) -> str:
    """Load a numbered prompt file from the Master Prompts folder."""
    pattern = os.path.join(PROMPTS_DIR, f"0{step_number}-*.md")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No prompt file found for step {step_number} in {PROMPTS_DIR}")
    return load_file(sorted(matches)[0])

def build_system_prompt(project_instructions: str, knowledge_base: str) -> str:
    return f"""{project_instructions}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KNOWLEDGE BASE — use this as your primary source of truth for all SpecTec-specific facts, brand guidelines, tone, and product information. Prioritise this over your training data.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{knowledge_base}
"""

def call_claude(client: anthropic.Anthropic, system: str, user_message: str, step_label: str) -> str:
    """Call the API with streaming and return the full response."""
    print(f"\n{'─'*60}")
    print(f"  Running {step_label}...")
    print(f"{'─'*60}")

    full_response = ""
    with client.messages.stream(
        model="claude-opus-4-5",
        max_tokens=4000,
        system=system,
        messages=[{"role": "user", "content": user_message}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print(f"\n\n  ✓ {step_label} complete ({len(full_response)} chars)")
    return full_response

def inject_inputs(prompt_template: str, inputs: dict) -> str:
    """Replace [paste here] placeholders in prompt templates with actual values."""
    result = prompt_template
    for key, value in inputs.items():
        result = result.replace(f"[{key}]", value)
    return result

def save_output(content: str, slug: str) -> str:
    """Save the compiled output document to /output/."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"{timestamp}-{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath

# ── Pipeline ──────────────────────────────────────────────────────────────────

def run_pipeline():
    print("\n" + "═"*60)
    print("  SPECTEC CONTENT PIPELINE")
    print("═"*60)

    # Validate API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n✗ ANTHROPIC_API_KEY environment variable not set.")
        print("  Run: export ANTHROPIC_API_KEY=your-key-here")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Load system prompt + knowledge base
    print("\n→ Loading system prompt...")
    project_instructions = load_file(SYSTEM_PROMPT_FILE)

    print("→ Loading knowledge base...")
    knowledge_base = load_knowledge_base()
    print(f"  Loaded {len(knowledge_base)} characters from knowledge base")

    system_prompt = build_system_prompt(project_instructions, knowledge_base)

    # Print run config
    print("\n→ Run configuration:")
    for k, v in INPUTS.items():
        print(f"  {k}: {v}")

    # ── STEP 01: SEO Brief ────────────────────────────────────────────────────
    prompt_01 = load_prompt(1)
    user_01 = inject_inputs(prompt_01, {
        "paste here": INPUTS["primary_keyword"],  # primary keyword slot
        "Primary keyword": INPUTS["primary_keyword"],
        "Secondary keywords": INPUTS["secondary_keywords"],
        "Intent": INPUTS["intent"],
        "Persona": INPUTS["persona"],
        "Business goal": INPUTS["business_goal"],
    })
    # Build clean prompt with explicit inputs
    user_01 = f"""INPUTS:
* Primary keyword: {INPUTS['primary_keyword']}
* Secondary keywords: {INPUTS['secondary_keywords']}
* Intent: {INPUTS['intent']}
* Persona: {INPUTS['persona']}
* Business goal: {INPUTS['business_goal']}

{prompt_01}"""

    brief = call_claude(client, system_prompt, user_01, "Step 01 — SEO Brief Builder")

    # ── STEP 02: Outline ──────────────────────────────────────────────────────
    prompt_02 = load_prompt(2)
    user_02 = f"""INPUTS:
* SEO content brief from Step 01:

{brief}

{prompt_02}"""

    outline = call_claude(client, system_prompt, user_02, "Step 02 — Outline Architect")

    # ── STEP 03: Research Pack ────────────────────────────────────────────────
    prompt_03 = load_prompt(3)
    user_03 = f"""INPUTS:
* SEO content brief from Step 01:

{brief}

* Approved outline from Step 02:

{outline}

{prompt_03}"""

    research = call_claude(client, system_prompt, user_03, "Step 03 — Research & Evidence Pack")

    # ── STEP 04: Draft Writer ─────────────────────────────────────────────────
    prompt_04 = load_prompt(4)
    user_04 = f"""INPUTS:
* SEO brief from Step 01:

{brief}

* Outline from Step 02:

{outline}

* Research pack from Step 03:

{research}

{prompt_04}"""

    draft = call_claude(client, system_prompt, user_04, "Step 04 — Draft Writer")

    # ── STEP 05: SEO Optimiser & Repurposer ───────────────────────────────────
    prompt_05 = load_prompt(5)
    user_05 = f"""INPUTS:
* Reviewed article draft:

{draft}

{prompt_05}"""

    repurpose = call_claude(client, system_prompt, user_05, "Step 05 — SEO Optimiser & Repurposer")

    # ── Compile output document ───────────────────────────────────────────────
    slug = INPUTS["primary_keyword"].lower().replace(" ", "-")[:50]

    compiled = f"""# SpecTec Content Pipeline — Output
**Keyword:** {INPUTS['primary_keyword']}
**Intent:** {INPUTS['intent']} | **Persona:** {INPUTS['persona']} | **Goal:** {INPUTS['business_goal']}
**Generated:** {datetime.datetime.now().strftime("%d %B %Y, %H:%M")}

---

## Step 01 — SEO Brief

{brief}

---

## Step 02 — Outline

{outline}

---

## Step 03 — Research & Evidence Pack

{research}

---

## Step 04 — Article Draft

{draft}

---

## Step 05 — SEO Optimiser & Repurposing Pack

{repurpose}
"""

    output_path = save_output(compiled, slug)

    print("\n" + "═"*60)
    print("  PIPELINE COMPLETE")
    print(f"  Output saved to: {output_path}")
    print("═"*60 + "\n")

if __name__ == "__main__":
    run_pipeline()
