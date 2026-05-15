#!/usr/bin/env python3
"""
CALB-2 Curator Self-Consistency Checker (v1)
=============================================

Scans every case in a CALB-2 corpus and flags internal contradictions
between curator-authored fields. The output is a CSV of drift candidates
the curator can work through, ordered by severity.

This script is deliberately *self*-consistent: every rule is a logical
implication between two or more curator-authored fields. None of the
rules consult the engine's prediction. The output therefore measures
curator drift, not engine accuracy.

Rules
-----
R1 (HIGH):    sanctioned_entity_role == "joint" => >=2 liability slots > 0
R2 (HIGH):    sanctioned_entity_role == "individual" => human_operator > 0
R3 (HIGH):    sanctioned_entity_role == "firm" => deployer > 0 OR ai_provider > 0
R4 (MEDIUM):  sanctioned_entity_role == "n/a" AND primary_source_type IS
              POPULATED (=> we have evidence of no-sanction, not missing data)
              => regulator > 0 OR affected_party > 0
              (excused for civil-tort categories)
R5 (MEDIUM):  failure_category in {intellectual_property, privacy_violation}
              => ai_provider > 0 OR affected_party > 0 (defendant lost or
              plaintiff defeat)
R6a(HIGH):    model_provider explicitly "none"/"n/a"/"unknown" (curator intent
              signal) AND ai_provider > 0 => contradiction
R6b(LOW):     model_provider IS NULL (data-completeness gap, not a
              contradiction) AND ai_provider > 0 => fill-in candidate
R7 (CRIT):    sum(liability_allocation.values()) MUST equal 100
              (data integrity, not strictly a contradiction)

Gap-tracking pass
-----------------
In addition to rule violations, the script reports two systemic
data-completeness counts that are *not* contradictions but indicate
curator-workflow gaps the maintainer may want to address:

  G1: number of cases with primary_source_type IS NULL
  G2: number of cases with model_provider IS NULL

Usage
-----
    python3 consistency_check.py [<corpus_path>] [-o <out_csv>]

Default corpus path: /home/ubuntu/calb2/v09/calb2_v09.json
Default output:      drift_candidates_v1.csv (in cwd)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_CORPUS = "/home/ubuntu/calb2/v09/calb2_v09.json"
DEFAULT_OUTPUT = "drift_candidates_v1.csv"

ALLOC_SLOTS = (
    "ai_provider",
    "deployer",
    "human_operator",
    "data_provider",
    "regulator",
    "external_actor",
    "affected_party",
)

NULLISH = {"", "none", "null", "n/a", "na"}

CIVIL_TORT_CATEGORIES = {
    "private_dispute",
    "tort_claim",
    "personal_injury",
    "negligence",
}


def is_null(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip().lower() in NULLISH
    return False


def alloc_int(la: dict, slot: str) -> int:
    val = la.get(slot, 0)
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0


def check_case(c: dict) -> list[dict]:
    """Run all rules on a single case; return a list of violation records."""
    case_id = c.get("id") or c.get("case_id") or "?"
    title = (c.get("title") or "")[:60]
    ts = c.get("telemetry_signals", {}) or {}
    la = c.get("liability_allocation", {}) or {}

    role = str(ts.get("sanctioned_entity_role", "")).lower().strip()
    provider = ts.get("model_provider")
    failure = str(c.get("failure_category", "")).lower().strip()

    nonzero_slots = [s for s in ALLOC_SLOTS if alloc_int(la, s) > 0]
    total = sum(alloc_int(la, s) for s in ALLOC_SLOTS)

    violations: list[dict] = []

    def flag(rule: str, severity: str, detail: str) -> None:
        violations.append({
            "case_id": case_id,
            "title": title,
            "rule": rule,
            "severity": severity,
            "sanctioned_entity_role": role or "(empty)",
            "model_provider": provider if provider not in (None, "") else "(null)",
            "failure_category": failure or "(empty)",
            "liability_allocation": "; ".join(
                f"{s}={alloc_int(la, s)}" for s in ALLOC_SLOTS if alloc_int(la, s) > 0
            ) or "(all zero)",
            "alloc_total": total,
            "detail": detail,
        })

    # R1 — joint sanction must show in >=2 slots
    if role == "joint" and len(nonzero_slots) < 2:
        flag(
            "R1_joint_sanction_must_show_in_2plus_slots",
            "HIGH",
            f"role=joint but only {len(nonzero_slots)} slot(s) nonzero: {nonzero_slots}",
        )

    # R2 — individual sanction must include human_operator
    if role == "individual" and alloc_int(la, "human_operator") == 0:
        flag(
            "R2_individual_sanction_must_include_human_operator",
            "HIGH",
            "role=individual but human_operator==0",
        )

    # R3 — firm sanction must include deployer or ai_provider
    if role == "firm" and alloc_int(la, "deployer") == 0 and alloc_int(la, "ai_provider") == 0:
        flag(
            "R3_firm_sanction_must_include_deployer_or_ai_provider",
            "HIGH",
            "role=firm but deployer==0 AND ai_provider==0",
        )

    # R4 — n/a sanction WITH evidence (populated source type) must surface
    # regulator or affected_party slot. Excused for civil-tort categories.
    src_type = c.get("primary_source_type")
    src_type_populated = not is_null(src_type)
    if role in ("n/a", "na") and src_type_populated and failure not in CIVIL_TORT_CATEGORIES:
        if alloc_int(la, "regulator") == 0 and alloc_int(la, "affected_party") == 0:
            flag(
                "R4_no_sanction_must_surface_regulator_or_affected_party",
                "MEDIUM",
                f"role=n/a, source_type={src_type}, failure={failure}, but regulator==0 AND affected_party==0",
            )

    # R5 — IP / privacy cases must surface ai_provider OR affected_party
    if failure in ("intellectual_property", "privacy_violation"):
        if alloc_int(la, "ai_provider") == 0 and alloc_int(la, "affected_party") == 0:
            flag(
                "R5_ip_or_privacy_must_surface_ai_provider_or_affected_party",
                "MEDIUM",
                f"failure={failure}, but ai_provider==0 AND affected_party==0",
            )

    # R6a — explicit "none" provider cannot have ai_provider liability (real contradiction)
    if isinstance(provider, str) and provider.strip().lower() in {"none", "n/a", "na", "unknown"} and alloc_int(la, "ai_provider") > 0:
        flag(
            "R6a_explicit_none_provider_cannot_have_ai_provider_liability",
            "HIGH",
            f"model_provider={provider!r} but ai_provider={alloc_int(la, 'ai_provider')}",
        )
    # R6b — null provider with ai_provider liability (data-completeness fill-in)
    if provider is None and alloc_int(la, "ai_provider") > 0:
        flag(
            "R6b_null_provider_fillin_candidate",
            "LOW",
            f"model_provider=null but ai_provider={alloc_int(la, 'ai_provider')} — fill in vendor name",
        )

    # R7 — allocation must sum to 100
    if total != 100:
        flag(
            "R7_allocation_must_sum_to_100",
            "CRITICAL",
            f"sum(liability_allocation) = {total} (expected 100)",
        )

    return violations


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus", nargs="?", default=DEFAULT_CORPUS)
    ap.add_argument("-o", "--output", default=DEFAULT_OUTPUT)
    args = ap.parse_args()

    with open(args.corpus, encoding="utf-8") as f:
        corpus = json.load(f)
    cases = corpus.get("cases") if isinstance(corpus, dict) else corpus

    all_violations: list[dict] = []
    for c in cases:
        all_violations.extend(check_case(c))

    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_violations.sort(key=lambda v: (severity_order.get(v["severity"], 9), v["rule"], v["case_id"]))

    fields = [
        "case_id", "title", "rule", "severity",
        "sanctioned_entity_role", "model_provider", "failure_category",
        "liability_allocation", "alloc_total", "detail",
    ]

    out_path = Path(args.output)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(all_violations)

    # Summary
    by_rule: dict[str, int] = {}
    by_sev: dict[str, int] = {}
    for v in all_violations:
        by_rule[v["rule"]] = by_rule.get(v["rule"], 0) + 1
        by_sev[v["severity"]] = by_sev.get(v["severity"], 0) + 1

    # Gap-tracking pass
    g1 = sum(1 for c in cases if is_null(c.get("primary_source_type")))
    g2 = sum(1 for c in cases if (c.get("telemetry_signals") or {}).get("model_provider") is None)

    print(f"corpus              : {args.corpus}")
    print(f"cases scanned       : {len(cases)}")
    print(f"violations found    : {len(all_violations)}")
    print(f"affected cases      : {len({v['case_id'] for v in all_violations})}")
    print()
    print("by severity:")
    for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        if sev in by_sev:
            print(f"  {sev:<10s} {by_sev[sev]}")
    print()
    print("by rule:")
    for rule, n in sorted(by_rule.items()):
        print(f"  {rule:<60s} {n}")
    print()
    print("data-completeness gaps (not contradictions):")
    print(f"  G1 cases with primary_source_type=null  {g1}")
    print(f"  G2 cases with model_provider=null       {g2}")
    print()
    print(f"output              : {out_path.resolve()}")
    return 0 if not by_sev.get("CRITICAL") else 1


if __name__ == "__main__":
    sys.exit(main())
