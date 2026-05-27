# SpecTec Content Engine

This repository is the production hub for all marketing content assets supporting the SpecTec go-to-market programme. It sits between strategy and distribution in a three-layer model:

```
Plan (strategy)  →  Content Engine (this repo)  →  Campaign Hub (distribution)
```

---

## What this repo is

The Content Engine is where content gets briefed, drafted, reviewed, and stored before it goes live. It holds:

- **Prompts** — reusable Claude prompts for every content type (email, social, long-form, sales enablement)
- **Knowledge base** — brand guidelines, value proposition, ICP, product data, and tone examples for use in AI-assisted production
- **Output** — finished or in-progress assets, organised by funnel stage
- **Assets** — tracking and reference files, including the master asset register
- **Pipeline** — the automation layer that connects Claude to the production workflow

---

## The three-layer model

### Layer 1 — Plan (upstream source of truth)
**[SpecTec Prospect to Lifecycle Plan 2026](https://stuartedmondson.github.io/SpecTec_Prospect_to_Lifecycle_Plan_2026/)**

The Plan defines the full end-to-end customer journey from first prospect touch to long-term lifecycle. It specifies which assets are needed at each stage, which streams they serve, and the current build status. All prioritisation decisions originate here. If an asset exists in the Plan, it belongs in this Content Engine.

### Layer 2 — Content Engine (this repo)
This repository. Receives requirements from the Plan, produces finished assets, and routes them to the Campaign Hub. Prompt files, knowledge base materials, and the asset register all live here.

### Layer 3 — Campaign Hub (downstream distribution)
The Campaign Hub receives finished assets from the Content Engine and distributes them — into HubSpot sequences, campaigns, sales playbooks, and web pages. Content does not go directly from production to the Campaign Hub without passing through this repo first.

---

## Repo structure

```
spectec-content-engine/
├── assets/
│   └── asset-register.md        # Master asset tracking register (see below)
├── knowledge-base/
│   ├── product/                 # Product-specific data (AMOS stats, feature docs)
│   ├── email-templates/         # HTML email templates
│   ├── spectec-brand-guidelines
│   ├── spectec-value-proposition-text
│   ├── spectec-ideal-custome-profile-text
│   ├── spectec-amos-tier-brochure-(march-26)
│   └── tone-example-*.md        # Writing tone and voice reference files
├── output/
│   ├── stage-0-demand-creation/
│   ├── stage-1-attract-capture/
│   ├── stage-2-3-nurture-qualify/
│   ├── stage-4-deal-stage/
│   │   ├── stream-a-no-system/
│   │   ├── stream-b-competitor/
│   │   └── stream-c-legacy-amos/
│   ├── stage-5-onboarding/
│   ├── stage-6-7-lifecycle/
│   │   ├── decision-maker/
│   │   └── user-pathway/
│   └── services/
│       ├── sps-strategic-project/
│       └── support-tiers/
├── pipeline/                    # Automation layer — do not modify without review
│   ├── pipeline.py
│   └── config.py
├── project-instructions/        # Claude project-level instructions
├── prompts/
│   ├── Email/                   # Email prompt chain (01–05)
│   ├── Master Prompts/          # SEO and long-form prompt chain (01–05)
│   ├── Social Prompts/          # Social media prompt chain (01–05)
│   ├── longform/                # Long-form content prompts (new)
│   ├── sales-enablement/        # Sales enablement content prompts (new)
│   └── social/                  # Social content prompts (new)
└── changelog.md
```

### Folder purposes

| Folder | Purpose |
|--------|---------|
| `assets/` | Tracking files — the asset register lives here |
| `knowledge-base/` | Source material fed into AI prompts — brand, product, ICP, tone |
| `knowledge-base/product/` | Product-specific data: AMOS stats, feature comparisons |
| `output/` | Finished and in-progress content assets, organised by funnel stage |
| `pipeline/` | Python automation that runs the prompt pipeline — do not touch without checking with the pipeline owner |
| `prompts/` | Claude prompts by content type — used to brief and draft assets |
| `project-instructions/` | Claude project-level system instructions |

---

## How to use this repo

### Adding a new asset
1. Check the asset register at [`assets/asset-register.md`](assets/asset-register.md) — confirm the asset is listed and note its Output Path
2. Use the relevant prompt chain from `prompts/` to brief and draft
3. Save the finished file to the correct `output/` subfolder
4. Update the asset register: change Status from `Not Started` → `In Progress` → `Complete`
5. Add an entry to `changelog.md`

### Updating asset status
Open [`assets/asset-register.md`](assets/asset-register.md) and update the Status column for the relevant row. Status options:

| Status | Meaning |
|--------|---------|
| `Live` | Published and active |
| `Complete` | Finished and ready to deploy |
| `In Progress` | Currently being worked on |
| `Planned` | Scheduled, not yet started |
| `Not Started` | No work begun |

### Adding a new knowledge-base file
Save to the appropriate subfolder under `knowledge-base/`. For product data (stats, feature docs, competitive intel), use `knowledge-base/product/`.

### Running the pipeline
See [`pipeline/readme.md`](pipeline/readme.md) for pipeline setup and usage instructions.

---

## Asset register

The master asset register is at **[`assets/asset-register.md`](assets/asset-register.md)**.

It tracks every deliverable from the Prospect to Lifecycle Plan 2026 — name, type, priority, status, owner, and output path. All Stage 4 (Deal Stage) assets are marked Priority: HIGH as these are the current build focus through June 2026.
