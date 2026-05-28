import json
import re
from datetime import datetime, timezone


STATUS_MAP = {
    "live": "live",
    "complete": "complete",
    "in progress": "in_progress",
    "planned": "planned",
    "not started": "not_started",
}


def normalize_status(raw):
    return STATUS_MAP.get(raw.strip().lower(), raw.strip().lower().replace(" ", "_"))


def parse_stage_heading(heading):
    h = heading.strip()
    if re.search(r"Stage 0", h, re.I):
        return "demand"
    if re.search(r"Stage 1", h, re.I):
        return "capture"
    if re.search(r"Stages?\s*2", h, re.I):
        return "nurture"
    if re.search(r"Stage 4", h, re.I):
        return "deal"
    if re.search(r"Stage 5", h, re.I):
        return "onboarding"
    if re.search(r"Stages?\s*6", h, re.I):
        return "lifecycle"
    if re.search(r"Support Tiers?", h, re.I):
        return "support"
    if re.search(r"Services?", h, re.I):
        return "services"
    return None


def parse_row(line):
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    if len(parts) < 6:
        return None
    stage, name, asset_type, priority, status, owner = parts[:6]
    output_path = parts[6].strip() if len(parts) > 6 else ""
    notes = parts[7].strip() if len(parts) > 7 else ""
    if not name or re.match(r"-+", name) or name.lower() == "asset name":
        return None
    return {
        "title": name,
        "type": asset_type,
        "priority": priority,
        "status": normalize_status(status),
        "owner": owner,
        "notes": notes,
    }


def detect_stream(heading):
    h = heading.lower()
    if "stream a" in h or "no system" in h:
        return "A"
    if "stream b" in h or "competitor" in h:
        return "B"
    if "stream c" in h or "legacy" in h:
        return "C"
    return None


def main():
    with open("assets/asset-register.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    stages = {
        "demand": [],
        "capture": [],
        "nurture": [],
        "deal": [],
        "onboarding": [],
        "lifecycle": [],
        "services": [],
        "support": [],
    }

    current_stage = None
    current_stream = None

    for line in lines:
        line = line.rstrip("\n")

        if line.startswith("## "):
            heading = line[3:]
            new_stage = parse_stage_heading(heading)
            if new_stage:
                current_stage = new_stage
                current_stream = None
            continue

        if line.startswith("### "):
            heading = line[4:]
            if current_stage == "deal":
                current_stream = detect_stream(heading)
            continue

        if line.startswith("|") and current_stage:
            asset = parse_row(line)
            if asset:
                if current_stage == "deal" and current_stream:
                    asset["stream"] = current_stream
                stages[current_stage].append(asset)

    all_assets = [a for arr in stages.values() for a in arr]

    summary = {
        "live": sum(1 for a in all_assets if a["status"] == "live"),
        "complete": sum(1 for a in all_assets if a["status"] == "complete"),
        "in_progress": sum(1 for a in all_assets if a["status"] == "in_progress"),
        "planned": sum(1 for a in all_assets if a["status"] == "planned"),
        "not_started": sum(1 for a in all_assets if a["status"] == "not_started"),
    }

    manifest = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": summary,
        "stages": stages,
    }

    with open("content-manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    total = len(all_assets)
    print(f"Manifest generated: {total} assets")
    print(f"  live={summary['live']} complete={summary['complete']} "
          f"in_progress={summary['in_progress']} planned={summary['planned']} "
          f"not_started={summary['not_started']}")


if __name__ == "__main__":
    main()
