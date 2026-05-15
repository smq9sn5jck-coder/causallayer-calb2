#!/usr/bin/env python3
"""Compute v0.6 → v0.7 deltas with charts."""
import json
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

V07_MAP = "/home/ubuntu/engine_scan/cl-main/reports/calb2_v04_v08_scenario_map.json"
CORPUS = "/home/ubuntu/calb2/v07/calb2_v07.json"
OUT = Path("/home/ubuntu/calb2/v07/analysis")
OUT.mkdir(parents=True, exist_ok=True)

with open(V07_MAP) as f:
    cases = json.load(f)
with open(CORPUS) as f:
    corpus = json.load(f)
case_meta = {c["id"]: c for c in corpus["cases"]}

total = len(cases)
correct = 0
high_conf_total = 0
high_conf_correct = 0
l1_sum = 0
per_cat = defaultdict(lambda: {"total": 0, "correct": 0, "l1_sum": 0})
misses = []

for c in cases:
    cid = c["case_id"]
    meta = case_meta.get(cid, {})
    cat = meta.get("failure_category", "unknown")
    confidence = meta.get("ground_truth_confidence", "high")
    is_match = c.get("legal_primary_match", False)
    l1 = c.get("legal_l1_distance", 0)
    if is_match:
        correct += 1
    else:
        misses.append({"case_id": cid, "category": cat, "confidence": confidence,
                       "predicted": c.get("predicted_primary_legal"),
                       "ground_truth": c.get("ground_truth_primary_legal"),
                       "doctrine": c.get("applied_doctrine")})
    l1_sum += l1
    per_cat[cat]["total"] += 1
    if is_match:
        per_cat[cat]["correct"] += 1
    per_cat[cat]["l1_sum"] += l1
    if confidence == "high":
        high_conf_total += 1
        if is_match:
            high_conf_correct += 1

findings = {
    "engine_version": "1.0.0",
    "corpus_version": "calb2_v0.7",
    "total_cases": total,
    "legal_top1_accuracy_pct": round(100 * correct / total, 1),
    "legal_top1_high_confidence_pct": round(100 * high_conf_correct / high_conf_total, 1) if high_conf_total else 0,
    "high_confidence_n": high_conf_total,
    "low_confidence_n": total - high_conf_total,
    "mean_legal_l1_distance": round(l1_sum / total, 1),
    "per_category": {k: {"n": v["total"], "correct": v["correct"], 
                         "accuracy_pct": round(100 * v["correct"] / v["total"], 1) if v["total"] else 0,
                         "mean_l1": round(v["l1_sum"] / v["total"], 1) if v["total"] else 0}
                     for k, v in sorted(per_cat.items())},
    "remaining_misses_count": len(misses),
    "remaining_misses_high_conf": sum(1 for m in misses if m["confidence"] == "high"),
    "remaining_misses_by_category": dict(sorted(((cat, sum(1 for m in misses if m["category"] == cat))
                                                  for cat in {m["category"] for m in misses}), key=lambda x: -x[1])),
}
with open(OUT / "findings_v07.json", "w") as f:
    json.dump(findings, f, indent=2)

# Cross-cycle progression chart
cycles = ["v0.7\n/v0.4", "v0.8\n/v0.4", "v0.8.1\n/v0.5", "v0.9\n/v0.5", "v0.9.1\n/v0.6", "v1.0\n/v0.6", "v1.0\n/v0.7"]
all_top1 = [75.9, 79.6, 87.6, 89.1, 81.7, 88.1, findings["legal_top1_accuracy_pct"]]
high_conf_top1 = [None, None, None, None, 88.4, 89.0, findings["legal_top1_high_confidence_pct"]]
mean_l1s = [48.2, 38.9, 23.6, 20.7, 39.2, 26.0, findings["mean_legal_l1_distance"]]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(cycles, all_top1, marker="o", linewidth=2, label="All cases", color="#2E86AB")
hc_cycles = [c for c, v in zip(cycles, high_conf_top1) if v is not None]
hc_vals = [v for v in high_conf_top1 if v is not None]
axes[0].plot(hc_cycles, hc_vals, marker="s", linewidth=2, label="High-confidence subset", color="#43AA8B")
axes[0].set_title("Legal Top-1 Accuracy (cross-cycle)", fontsize=13)
axes[0].set_ylabel("Accuracy (%)")
axes[0].set_ylim(60, 100)
axes[0].legend()
axes[0].grid(True, alpha=0.3)
for i, v in enumerate(all_top1):
    axes[0].annotate(f"{v}%", (i, v), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=8, color="#2E86AB")
for i, c in enumerate(cycles):
    if high_conf_top1[i] is not None:
        axes[0].annotate(f"{high_conf_top1[i]}%", (i, high_conf_top1[i]), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8, color="#43AA8B")

axes[1].plot(cycles, mean_l1s, marker="s", linewidth=2, color="#A23B72")
axes[1].set_title("Mean Legal L1 Distance (lower=better)", fontsize=13)
axes[1].set_ylabel("Mean L1 / 200")
axes[1].set_ylim(10, 60)
axes[1].grid(True, alpha=0.3)
for i, v in enumerate(mean_l1s):
    axes[1].annotate(f"{v}", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)

plt.suptitle("CausalLayer Cross-Cycle Progression", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(OUT / "cross_cycle_v07.png", dpi=140, bbox_inches="tight")
plt.close()

# Per-category v0.7 chart
cats = sorted(findings["per_category"].keys())
n = [findings["per_category"][c]["n"] for c in cats]
acc = [findings["per_category"][c]["accuracy_pct"] for c in cats]
colors = ["#2E86AB" if a >= 90 else "#F18F01" if a >= 70 else "#A23B72" for a in acc]
fig, ax = plt.subplots(figsize=(13, 7))
bars = ax.barh(cats, acc, color=colors)
ax.set_xlabel("Legal Top-1 Accuracy (%)")
ax.set_title("Engine v1.0 / CALB-2 v0.7 — Per-Category Legal Accuracy", fontsize=13)
ax.set_xlim(0, 105)
ax.axvline(x=findings["legal_top1_accuracy_pct"], color="green", linestyle="--", alpha=0.7,
           label=f"Overall {findings['legal_top1_accuracy_pct']}%")
ax.axvline(x=findings["legal_top1_high_confidence_pct"], color="darkgreen", linestyle=":", alpha=0.7,
           label=f"High-conf {findings['legal_top1_high_confidence_pct']}%")
ax.legend(loc="lower right")
for bar, val, n_ in zip(bars, acc, n):
    ax.text(val + 1, bar.get_y() + bar.get_height() / 2, f"{val}% (n={n_})", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(OUT / "per_category_v07.png", dpi=140, bbox_inches="tight")
plt.close()

print("=== v1.0 / CALB-2 v0.7 ===")
print(json.dumps(findings, indent=2))
print(f"\nCharts written to {OUT}")
