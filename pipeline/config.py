# SpecTec Content Pipeline — Configuration
# Fill in your inputs here before running pipeline.py

INPUTS = {
    "primary_keyword":    "ship maintenance software",
    "secondary_keywords": "planned maintenance system, PMS software maritime, vessel maintenance management, predictive maintenance shipping",
    "intent":             "MOFU",
    "persona":            "Functional Specialist",
    "business_goal":      "Consideration",
}

# File paths (relative to repo root)
KNOWLEDGE_BASE_DIR  = "knowledge-base"
PROMPTS_DIR         = "prompts/Master Prompts"
SYSTEM_PROMPT_FILE  = "project-instructions/claude-project-instructions.md"
OUTPUT_DIR          = "output"
