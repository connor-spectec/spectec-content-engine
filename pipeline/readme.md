# SpecTec Content Pipeline

Automates the 5-step master content pipeline end-to-end using the Anthropic API.

## What it does

1. Loads your system prompt from `/project-instructions/`
2. Loads your entire knowledge base from `/knowledge-base/`
3. Runs your 5 master prompts in sequence — each step's output is automatically fed into the next
4. Saves a single compiled output document to `/output/`

## Setup (one time only)

**1. Install Python dependencies**
```bash
pip install anthropic
```

**2. Set your Anthropic API key**
```bash
export ANTHROPIC_API_KEY=your-key-here
```
To make this permanent, add it to your `~/.zshrc` or `~/.bashrc`.

**3. Clone the repo and navigate to root**
```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
```

## Running the pipeline

**1. Open `pipeline/config.py` and fill in your inputs:**
```python
INPUTS = {
    "primary_keyword":    "maritime asset management software",
    "secondary_keywords": "vessel maintenance software, CMMS maritime",
    "intent":             "TOFU",
    "persona":            "Executive",
    "business_goal":      "Awareness",
}
```

**2. Run from the repo root:**
```bash
python pipeline/pipeline.py
```

**3. Find your output in `/output/`**

Output files are named: `YYYYMMDD-HHMM-your-keyword.md`

## Output structure

Each output file contains all 5 steps compiled into a single document:
- Step 01 — SEO Brief
- Step 02 — Outline
- Step 03 — Research & Evidence Pack
- Step 04 — Article Draft
- Step 05 — SEO Optimiser & Repurposing Pack

## Folder dependencies

```
/knowledge-base/          ← all files loaded automatically
/project-instructions/
  claude-project-instructions.md
/prompts/
  /Master Prompts/
    01-seo-brief-builder.md
    02-outline-architect.md
    03-research-evidence-pack.md
    04-draft-writer.md
    05-seo-optimiser-repurposer.md
/output/                  ← generated files saved here
/pipeline/
  pipeline.py             ← main script
  config.py               ← your inputs go here
  README.md               ← this file
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ANTHROPIC_API_KEY not set` | Run `export ANTHROPIC_API_KEY=your-key` |
| `No prompt file found for step N` | Check filenames start with `0N-` in `/prompts/Master Prompts/` |
| `Could not read [filename]` | Check the file is plain text (not binary) |
| Rate limit errors | The script runs sequentially — if you hit limits, add `time.sleep(5)` between steps |
