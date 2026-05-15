#!/usr/bin/env python3
"""
CIDL Layer 1 corpus validator.

Validates the CALB-2 corpus against the closed-enum schema defined in
schema/cidl-layer1.schema.json. Reports per-case errors and warnings.

Exit code 0 on clean validation, 1 on any errors.

Usage:
    python3 scripts/validate_cidl_layer1.py [<corpus_path>] [-o <out_csv>]
"""

from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schema" / "cidl-layer1.schema.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="CIDL Layer 1 corpus validator")
    ap.add_argument("corpus", nargs="?", default=str(REPO_ROOT / "calb2_v09.json"))
    ap.add_argument("-o", "--out", default=str(REPO_ROOT / "analysis" / "v1.6" / "cidl_layer1_violations.csv"))
    args = ap.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    with open(args.corpus, encoding="utf-8") as f:
        raw = json.load(f)
    cases = raw["cases"] if isinstance(raw, dict) else raw

    # Pull the closed enums out of the schema (single source of truth).
    fc_enum   = set(schema["properties"]["failure_category"]["enum"])
    pst_enum  = set(schema["properties"]["primary_source_type"]["enum"]) - {None}
    role_enum = set(schema["properties"]["telemetry_signals"]["properties"]["sanctioned_entity_role"]["enum"]) - {None}
    hitl_enum = set(schema["properties"]["telemetry_signals"]["properties"]["human_in_the_loop"]["enum"]) - {None}
    pred_enum = set(schema["properties"]["telemetry_signals"]["properties"]["incident_was_predictable"]["enum"]) - {None}
    kfm_enum  = set(schema["properties"]["telemetry_signals"]["properties"]["known_failure_modes_disclosed"]["enum"]) - {None}
    ovip_enum = set(schema["properties"]["telemetry_signals"]["properties"]["output_validation_in_place"]["enum"]) - {None}
    slots     = list(schema["properties"]["liability_allocation"]["properties"].keys())

    issues: list[dict] = []

    def add(case_id: str, field: str, sev: str, detail: str) -> None:
        issues.append({"case_id": case_id, "field": field, "severity": sev, "detail": detail})

    for c in cases:
        cid = c.get("id", "?")
        ts = c.get("telemetry_signals") or {}
        la = c.get("liability_allocation") or {}

        # required string fields
        for required in ("title", "incident_description", "jurisdiction", "domain", "ai_system_type"):
            if not isinstance(c.get(required), str) or not c.get(required):
                add(cid, required, "error", f"missing or non-string required field")

        # failure_category (enum, required)
        fc = c.get("failure_category")
        if fc not in fc_enum:
            add(cid, "failure_category", "error", f"value {fc!r} not in CIDL enum")

        # primary_source_type (enum, nullable)
        pst = c.get("primary_source_type")
        if pst is not None and pst not in pst_enum:
            add(cid, "primary_source_type", "error", f"value {pst!r} not in CIDL enum")

        # sanctioned_entity_role (enum, nullable)
        role = ts.get("sanctioned_entity_role")
        if role is not None and role not in role_enum:
            add(cid, "telemetry_signals.sanctioned_entity_role", "error", f"value {role!r} not in CIDL enum")

        # tristate fields
        for f, allowed in (
            ("human_in_the_loop", hitl_enum),
            ("incident_was_predictable", pred_enum),
            ("known_failure_modes_disclosed", kfm_enum),
            ("output_validation_in_place", ovip_enum),
        ):
            v = ts.get(f)
            if v is not None and v not in allowed:
                add(cid, f"telemetry_signals.{f}", "error", f"value {v!r} not in CIDL enum {sorted(allowed)}")

        # liability_allocation
        if not isinstance(la, dict):
            add(cid, "liability_allocation", "error", "missing or non-object")
            continue
        total = 0
        for slot in slots:
            v = la.get(slot, 0)
            if not isinstance(v, int) or v < 0 or v > 100:
                add(cid, f"liability_allocation.{slot}", "error", f"expected int 0-100, got {v!r}")
            else:
                total += v
        for k in la.keys():
            if k not in slots:
                add(cid, f"liability_allocation.{k}", "warn", "unknown slot key not in CIDL Layer 1")
        if total != 100:
            add(cid, "liability_allocation", "error", f"slots sum to {total}, expected 100")

    # Output
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["case_id", "field", "severity", "detail"])
        w.writeheader()
        w.writerows(issues)

    errors = sum(1 for i in issues if i["severity"] == "error")
    warns  = sum(1 for i in issues if i["severity"] == "warn")
    print(f"corpus           : {args.corpus}")
    print(f"schema           : {SCHEMA_PATH}")
    print(f"cases scanned    : {len(cases)}")
    print(f"errors           : {errors}")
    print(f"warnings         : {warns}")
    print(f"affected cases   : {len({i['case_id'] for i in issues})}")
    print(f"output           : {out_path.resolve()}")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
