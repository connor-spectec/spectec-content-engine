# SpecTec Content Pipeline — Configuration
# Fill in your inputs here before running pipeline.py

# ── Your content inputs ───────────────────────────────────────────────────────

INPUTS = {
    "primary_keyword":   "maritime asset management software",   # required
    "secondary_keywords": "vessel maintenance software, CMMS maritime",  # or "none"
    "intent":            "TOFU",       # TOFU / MOFU / BOFU
    "persona":           "Executive",  # Executive / Operational Leadership / Functional Specialist / Operator
    "business_goal":     "Awareness",  # Awareness / Consideration / Conversion / Upsell / Retention
}

# ── File paths (relative to repo root) ───────────────────────────────────────
# Update these if your folder names differ

KNOWLEDGE_BASE_DIR  = "knowledge-base"
PROMPTS_DIR         = "prompts/Master Prompts"
SYSTEM_PROMPT_FILE  = "project-instructions/claude-project-instructions.md"
OUTPUT_DIR          = "output"
