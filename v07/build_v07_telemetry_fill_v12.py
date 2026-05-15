#!/usr/bin/env python3
"""
v1.2 telemetry fill pass for CALB-2 v0.7.

The v1.2 calibration pass already relabeled L2-016 and L5-002. This pass
fills the missing telemetry fields the engine needs to apply the v1.2
doctrine fixes:
  - L5-104 (ICO Royal Free / DeepMind): primary_source_type=regulator_order,
    primary_source_citation pointing at ICO undertaking
  - L6-903 (PIPC v Facebook): model_provider="in-house", deployer_org="Facebook",
    primary_source_citation
  - L6-905 (ICO v TikTok): model_provider="in-house", deployer_org="TikTok",
    primary_source_citation
  - L9-906 (BEA Air France 447): primary_source_citation references "BEA"
    so the v1.2 aviation safety-board branch fires; ensure model_provider
    and deployer_org are set so engine can route to ai_provider/human_operator.

These are NOT new doctrine inventions; they are curator data fills that
should have been there from L0/L1 curation.

Outputs to calb2_v07.json (in place) and recomputes the SHA-256 hash.
"""
import json
import hashlib
import copy
import sys
from pathlib import Path

CORPUS = Path("/home/ubuntu/calb2/v07/calb2_v07.json")

CHANGES = {
    "L5-104": {
        # ICO Undertaking, July 2017 (Royal Free / DeepMind Streams)
        "primary_source_type": "regulator_order",
        "primary_source_citation": "ICO Undertaking against Royal Free London NHS Foundation Trust (3 July 2017)",
        "primary_business_model": "ai_as_operations",  # NHS deploys AI for operations
        "sanctioned_entity_role": "firm",
    },
    "L6-903": {
        # PIPC (Korea) Personal Information Protection Commission v Facebook, 2021
        "model_provider": "in-house",
        "deployer_org": "Facebook",
        "primary_source_citation": "PIPC v Facebook (2021), Korea PIPC administrative penalty for Photo Tag Suggest",
    },
    "L6-905": {
        # ICO v TikTok, April 2023 — UK GDPR fine for under-13s data processing
        "model_provider": "in-house",
        "deployer_org": "TikTok",
        "primary_source_citation": "ICO Monetary Penalty Notice against TikTok Information Technologies UK Ltd (4 April 2023)",
    },
    "L9-906": {
        # BEA Final Report on AF447, July 2012
        "model_provider": "Airbus",
        "deployer_org": "Air France",
        "primary_source_citation": "BEA Final Report on the accident on 1st June 2009 to the Airbus A330-203 registered F-GZCP operated by Air France flight AF 447 Rio de Janeiro – Paris (July 2012)",
    },
}


def main() -> int:
    data = json.loads(CORPUS.read_text())
    cases = data["cases"] if isinstance(data, dict) else data
    # v1.2 also fixes the top-level primary_source_citation for L5-104 since
    # the runner pulls the top-level field. The original wording '...Trust and
    # DeepMind' misled the engine's joint-respondent detector. The formal ICO
    # undertaking was issued only against the Trust as data controller.
    TOP_LEVEL_FIXES = {
        "L5-104": {
            "primary_source_citation": "ICO Undertaking against Royal Free London NHS Foundation Trust (3 July 2017)",
        },
        # L2-016: top-level pointed to the UK Upper Tribunal appellate decision
        # ([2025] UKUT 319 (AAC)), which led the engine to treat it as a court
        # opinion rather than the underlying ICO regulator action. The operative
        # legal event is the ICO Monetary Penalty Notice against Clearview;
        # the appeal is downstream review.
        "L2-016": {
            "primary_source_type": "regulator_order",
            "primary_source_citation": "ICO Monetary Penalty Notice against Clearview AI Inc (May 2022)",
        },
    }

    touched = []
    for c in cases:
        cid = c.get("id")
        if cid in CHANGES:
            ts = c.setdefault("telemetry_signals", {})
            for k, v in CHANGES[cid].items():
                if ts.get(k) in (None, "", "n/a"):
                    ts[k] = v
                    touched.append((cid, k, v))
                else:
                    # Don't overwrite existing curator value
                    pass
        if cid in TOP_LEVEL_FIXES:
            for k, v in TOP_LEVEL_FIXES[cid].items():
                # Always overwrite top-level for the targeted fields — we are
                # explicitly correcting curator labelling that misled the engine.
                old = c.get(k)
                c[k] = v
                touched.append((cid, f"top.{k}", f"(was: {old!r})"))

    # Recompute corpus integrity hash (over cases array, deterministic JSON)
    if isinstance(data, dict):
        data["version"] = "0.7.2"
        cases_canonical = json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()
        data["sha256"] = hashlib.sha256(cases_canonical).hexdigest()
        out = data
    else:
        out = cases

    CORPUS.write_text(json.dumps(out, indent=2) + "\n")

    print(f"v1.2 telemetry fill: {len(touched)} field updates applied")
    for cid, k, v in touched:
        print(f"  {cid:8s} {k:30s} = {v[:60] if isinstance(v, str) else v}")
    if isinstance(data, dict):
        print(f"\ncorpus version : {data.get('version')}")
        print(f"corpus sha256  : {data.get('sha256')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
