#!/usr/bin/env python3
"""Extract every v1.0 miss on NEW v0.6-added cases (L*-9XX) with full context."""
import json
from pathlib import Path

SCEN = "/home/ubuntu/engine_scan/cl-main/reports/calb2_v04_v08_scenario_map.json"
CORPUS = "/home/ubuntu/calb2/v06/calb2_v06.json"
OUT = Path("/home/ubuntu/calb2/v07/v10_misses_new.txt")
OUT.parent.mkdir(parents=True, exist_ok=True)

with open(SCEN) as f:
    cases = json.load(f)
with open(CORPUS) as f:
    corpus = json.load(f)

case_meta = {c["id"]: c for c in corpus["cases"]}

def is_new_case(cid: str) -> bool:
    """A case added in v0.6 has the L*-9XX pattern."""
    return any(cid.startswith(f"L{n}-9") for n in range(1, 12))

new_misses = []
old_misses = []

for c in cases:
    cid = c["case_id"]
    if c.get("legal_primary_match"):
        continue
    if is_new_case(cid):
        new_misses.append(c)
    else:
        old_misses.append(c)

print(f"v1.0 misses: total={len(new_misses) + len(old_misses)}, on NEW cases={len(new_misses)}, on OLD (v0.5) cases={len(old_misses)}")

lines = []
lines.append("=" * 78)
lines.append(f"v1.0 MISSES ON NEW v0.6 CASES — total {len(new_misses)}")
lines.append("=" * 78)

for m in new_misses:
    cid = m["case_id"]
    meta = case_meta.get(cid, {})
    lines.append("")
    lines.append("-" * 78)
    lines.append(f"CASE: {cid}  |  {meta.get('title', m.get('title', '?'))}")
    lines.append(f"  failure_category    : {m.get('failure_category')}")
    lines.append(f"  domain              : {m.get('domain')}")
    lines.append(f"  predicted (legal)   : {m.get('predicted_primary_legal')} — alloc {m.get('predicted_legal_attribution')}")
    lines.append(f"  ground truth (legal): {m.get('ground_truth_primary_legal')} — alloc {m.get('legal_ground_truth')}")
    lines.append(f"  L1 distance         : {m.get('legal_l1_distance')}")
    lines.append(f"  applied doctrine    : {m.get('applied_doctrine')}")
    lines.append(f"  primary_business_model: {meta.get('primary_business_model')}")
    lines.append(f"  primary_source_type : {meta.get('primary_source_type')}")
    sa = meta.get("system_architecture", {})
    if isinstance(sa, dict):
        lines.append(f"  model_provider      : {sa.get('model_provider')}")
        lines.append(f"  deployer_org        : {sa.get('deployer_org')}")
    desc = meta.get("incident_description", "")
    lines.append(f"  description         : {desc[:280]}{'...' if len(desc) > 280 else ''}")
    if "primary_source_citation" in meta:
        lines.append(f"  citation            : {meta['primary_source_citation']}")
    if "primary_source_url" in meta:
        lines.append(f"  source URL          : {meta['primary_source_url']}")

lines.append("")
lines.append("=" * 78)
lines.append(f"v1.0 MISSES ON OLD v0.5 CASES — total {len(old_misses)}")
lines.append("=" * 78)
for m in old_misses:
    cid = m["case_id"]
    meta = case_meta.get(cid, {})
    lines.append(f"  {cid}: {meta.get('title','?')[:80]}  pred={m.get('predicted_primary_legal')} GT={m.get('ground_truth_primary_legal')} doc={m.get('applied_doctrine')[:50]}")

OUT.write_text("\n".join(lines))
print(f"Written: {OUT}")
