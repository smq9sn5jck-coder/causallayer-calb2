#!/usr/bin/env python3
"""
v1.2 corpus run analysis. Compares v1.2 results to v1.1 baseline,
generates summary + charts.
"""
import json
import csv
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

V12_MAP = Path("/home/ubuntu/engine_scan/cl-main/reports/calb2_v04_v08_scenario_map.json")
CORPUS = Path("/home/ubuntu/calb2/v07/calb2_v07.json")
OUT = Path("/home/ubuntu/calb2/v07/analysis_v12")
OUT.mkdir(parents=True, exist_ok=True)


def load_corpus():
    d = json.loads(CORPUS.read_text())
    cases = d["cases"] if isinstance(d, dict) else d
    return {c["id"]: c for c in cases}


def main() -> int:
    rows = json.loads(V12_MAP.read_text())
    corpus = load_corpus()

    total = len(rows)
    legal_hits = sum(1 for r in rows if r.get("legal_primary_match"))
    causal_hits = sum(1 for r in rows if r.get("causal_primary_match"))

    def conf(case_id):
        return (corpus.get(case_id, {}).get("ground_truth_confidence") or "").lower()

    hi_rows = [r for r in rows if conf(r["case_id"]) == "high"]
    hi_legal_hits = sum(1 for r in hi_rows if r.get("legal_primary_match"))

    legal_misses = [r for r in rows if not r.get("legal_primary_match")]
    hi_misses = [r for r in legal_misses if conf(r["case_id"]) == "high"]

    by_doctrine = defaultdict(lambda: [0, 0])
    for r in rows:
        d = r.get("applied_doctrine") or "(none)"
        by_doctrine[d][1] += 1
        if r.get("legal_primary_match"):
            by_doctrine[d][0] += 1

    by_domain = defaultdict(lambda: [0, 0])
    for r in rows:
        d = r.get("domain") or "(unknown)"
        by_domain[d][1] += 1
        if r.get("legal_primary_match"):
            by_domain[d][0] += 1

    summary = []
    summary.append("# CALB-2 v0.7.2 / Engine v1.2.0 Run Summary")
    summary.append("")
    summary.append(f"Total cases : **{total}**  ")
    summary.append(f"Legal Top-1 (all)        : **{legal_hits}/{total} = {100*legal_hits/total:.1f}%**  ")
    summary.append(f"Legal Top-1 (high-conf)  : **{hi_legal_hits}/{len(hi_rows)} = {100*hi_legal_hits/max(1,len(hi_rows)):.1f}%**  ")
    summary.append(f"Causal Top-1 (all)       : {causal_hits}/{total} = {100*causal_hits/total:.1f}%  ")
    summary.append("")
    summary.append("## Comparison vs v1.1")
    summary.append("")
    summary.append("| Metric | v1.1 (CALB-2 v0.7) | v1.2 (CALB-2 v0.7.2) | Δ |")
    summary.append("|---|---|---|---|")
    summary.append(f"| Legal Top-1 (all)         | 91.6% (185/202) | {100*legal_hits/total:.1f}% ({legal_hits}/{total}) | {100*legal_hits/total - 91.6:+.1f}pp |")
    summary.append(f"| Legal Top-1 (high-conf)   | 94.7% (143/151) | {100*hi_legal_hits/max(1,len(hi_rows)):.1f}% ({hi_legal_hits}/{len(hi_rows)}) | {100*hi_legal_hits/max(1,len(hi_rows)) - 94.7:+.1f}pp |")
    summary.append("")
    summary.append("## High-confidence legal misses\n")
    if not hi_misses:
        summary.append("(none)")
    else:
        for r in sorted(hi_misses, key=lambda x: x["case_id"]):
            summary.append(f"- **{r['case_id']}** {r['title']}  ")
            summary.append(f"  doctrine: `{r.get('applied_doctrine','-')}`  ")
            summary.append(f"  predicted={r['predicted_primary_legal']}, gt={r['ground_truth_primary_legal']}, L1={r['legal_l1_distance']}  ")
    summary.append("")

    summary.append("## All legal misses (n={})".format(len(legal_misses)))
    summary.append("")
    summary.append("| Case | Conf | Domain | Doctrine | Predicted | GT | L1 |")
    summary.append("|---|---|---|---|---|---|---|")
    for r in sorted(legal_misses, key=lambda x: x["case_id"]):
        c = conf(r["case_id"])
        summary.append(f"| {r['case_id']} | {c} | {r.get('domain', '')} | `{r.get('applied_doctrine','-')}` | {r['predicted_primary_legal']} | {r['ground_truth_primary_legal']} | {r['legal_l1_distance']} |")
    summary.append("")

    summary.append("## Per-doctrine accuracy")
    summary.append("")
    summary.append("| Doctrine | Hits/Total | Acc |")
    summary.append("|---|---|---|")
    for d, (h, t) in sorted(by_doctrine.items(), key=lambda x: -x[1][1]):
        summary.append(f"| {d} | {h}/{t} | {100*h/t:.1f}% |")
    summary.append("")

    summary.append("## Per-domain accuracy")
    summary.append("")
    summary.append("| Domain | Hits/Total | Acc |")
    summary.append("|---|---|---|")
    for d, (h, t) in sorted(by_domain.items(), key=lambda x: -x[1][1]):
        summary.append(f"| {d} | {h}/{t} | {100*h/t:.1f}% |")
    (OUT / "summary_v12.md").write_text("\n".join(summary) + "\n")

    # CSV of misses
    with (OUT / "legal_misses_v12.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "confidence", "title", "domain", "doctrine", "predicted", "gt", "L1"])
        for r in sorted(legal_misses, key=lambda x: x["case_id"]):
            w.writerow([r["case_id"], conf(r["case_id"]), r["title"], r.get("domain", ""),
                        r.get("applied_doctrine", ""), r["predicted_primary_legal"],
                        r["ground_truth_primary_legal"], r["legal_l1_distance"]])

    # v1.1 hi-conf miss disposition
    targets = {
        "L2-016": "Calibration + engine (top-level citation, in-house, stop-words)",
        "L5-002": "Engine fix (FRCP-11 guard for regulator sources)",
        "L5-104": "Engine fix (tightened co-respondent) + corpus citation correction",
        "L6-903": "Engine fix (in-house provider detection)",
        "L6-905": "Engine fix (in-house provider detection)",
        "L9-906": "Engine fix (BEA aviation Level-2 branch)",
        "L7-001": "Accept as noise (n=1 publisher liability)",
        "L2-116": "Accept as noise (curator inconsistency with State v Pickett)",
    }
    by_id = {r["case_id"]: r for r in rows}
    tgt = ["## v1.1 hi-conf miss disposition under v1.2", ""]
    tgt.append("| Case | Plan | v1.2 result | Doctrine fired |")
    tgt.append("|---|---|---|---|")
    fixed = 0
    for cid, plan in targets.items():
        r = by_id.get(cid)
        if r is None:
            tgt.append(f"| {cid} | {plan} | (not found) | - |")
            continue
        ok = "✓ FIXED" if r["legal_primary_match"] else "✗ STILL MISS"
        if r["legal_primary_match"]:
            fixed += 1
        tgt.append(f"| {cid} | {plan} | {ok} | `{r.get('applied_doctrine','-')}` |")
    tgt.append("")
    tgt.append(f"**Resolved: {fixed}/8 targeted hi-conf misses (the remaining 2 are documented noise, not engine bugs).**")
    (OUT / "v11_target_dispositions.md").write_text("\n".join(tgt) + "\n")

    # Chart 1: accuracy progression
    versions = ["v0.7", "v0.8", "v0.8.1", "v0.9", "v1.0/v0.6", "v1.0/v0.7", "v1.1/v0.7", "v1.2/v0.7.2"]
    all_acc = [75.9, 79.6, 87.6, 89.1, 88.1, 89.6, 91.6, 100*legal_hits/total]
    hi_acc  = [None, None, None, None, None, 93.4, 94.7, 100*hi_legal_hits/max(1,len(hi_rows))]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    x = list(range(len(versions)))
    ax.plot(x, all_acc, marker="o", linewidth=2, label="All cases", color="#2563eb")
    hx = [i for i, v in enumerate(hi_acc) if v is not None]
    hy = [v for v in hi_acc if v is not None]
    ax.plot(hx, hy, marker="s", linewidth=2, label="High-confidence subset", color="#dc2626")
    for i, v in enumerate(all_acc):
        ax.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, 7), fontsize=9, ha="center", color="#2563eb")
    for i, v in zip(hx, hy):
        ax.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, -15), fontsize=9, ha="center", color="#dc2626")
    ax.set_xticks(x)
    ax.set_xticklabels(versions, rotation=20, ha="right")
    ax.set_ylim(70, 100)
    ax.set_ylabel("Legal Top-1 accuracy (%)")
    ax.set_title("CausalLayer Engine — Legal Top-1 Accuracy on CALB-2 (v0.7 → v1.2)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "accuracy_progression_v12.png", dpi=150)
    plt.close(fig)

    # Chart 2: per-domain accuracy bar (v1.2 only)
    fig, ax = plt.subplots(figsize=(11, 5.5))
    items = sorted(by_domain.items(), key=lambda x: -x[1][1])
    items = [(d, h, t) for d, (h, t) in items if t >= 3]
    labels = [d for d, _, _ in items]
    accs = [100*h/t for _, h, t in items]
    counts = [t for _, _, t in items]
    bars = ax.bar(labels, accs, color="#2563eb")
    for b, a, n in zip(bars, accs, counts):
        ax.annotate(f"{a:.0f}% (n={n})", xy=(b.get_x() + b.get_width()/2, a), xytext=(0, 4),
                    textcoords="offset points", ha="center", fontsize=9)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylim(0, 110)
    ax.set_ylabel("Legal Top-1 accuracy (%)")
    ax.set_title("v1.2 Per-Domain Legal Top-1 Accuracy (domains with n≥3)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "per_domain_accuracy_v12.png", dpi=150)
    plt.close(fig)

    # Chart 3: 8 targets disposition
    fig, ax = plt.subplots(figsize=(10, 5))
    target_ids = list(targets.keys())
    statuses = ["FIXED" if by_id.get(cid, {}).get("legal_primary_match") else "MISS" for cid in target_ids]
    colors = ["#16a34a" if s == "FIXED" else "#dc2626" for s in statuses]
    ax.barh(target_ids[::-1], [1]*len(target_ids), color=colors[::-1])
    for i, (cid, s) in enumerate(zip(target_ids, statuses)):
        ax.annotate(s, xy=(0.5, len(target_ids) - 1 - i), ha="center", va="center",
                    color="white", fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_title("v1.1 hi-conf misses → v1.2 disposition")
    fig.tight_layout()
    fig.savefig(OUT / "targets_disposition_v12.png", dpi=150)
    plt.close(fig)

    print(f"Legal Top-1 (all)        : {legal_hits}/{total} = {100*legal_hits/total:.1f}%")
    print(f"Legal Top-1 (high-conf)  : {hi_legal_hits}/{len(hi_rows)} = {100*hi_legal_hits/max(1,len(hi_rows)):.1f}%")
    print(f"v1.1 targets fixed: {fixed}/8")
    print(f"Outputs in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
