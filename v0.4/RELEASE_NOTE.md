# CALB-2 v0.4 Release Note

**Date:** 15 May 2026
**Engine Version:** CausalLayer v0.7.0
**Corpus Size:** 137 cases (dual ground-truth)
**Bitcoin Anchor:** `733a76d2c8bbc10ebfbc0f576a4c95d897866fab758498872eb9ce86bdd1fc5c`

## The "Corpus Skew Unmasking" Release

CALB-2 v0.3 reported an 80.6% top-1 accuracy on the legal axis. While mathematically true, that number was inflated by corpus skew: 78% of the v0.3 corpus consisted of lawyer-hallucination cases (FRCP Rule 11), a doctrine where the engine fires near-perfectly.

A public benchmark of record must be honest about its own blind spots. In v0.4, we expanded the corpus by adding 34 non-hallucination cases across bias, perception, adversarial, sensor drift, and pipeline failures.

The result is the engine's **actual operating accuracy** on a more representative case mix.

### Headline Results (v0.7 engine over v0.4 corpus)

| Axis | Top-1 Accuracy | Mean L1 Distance |
|---|---|---|
| **Causal Axis** | 66.4% | 76.1 / 200 |
| **Legal Axis** | 75.9% | 48.2 / 200 |

*Note: The legal axis dropped from 80.6% to 75.9% as the corpus diversified. This is a feature, not a bug. The benchmark is now harder and more honest.*

### Per-Category Performance

The expanded corpus reveals exactly where the engine is strong and where it needs work.

**Strong Areas (Production-Ready):**
- **Hallucination** (n=79): Legal 87.3%, Causal 73.4%
- **Perception Failure** (n=7): Legal 85.7%, Causal 100.0%
- **Pipeline Integration** (n=5): Legal 80.0%
- **Bias / Discrimination** (n=12): Legal 66.7%, Causal 83.3%

**Weak Areas (v0.8 Priorities):**
- **Specification Failure** (n=5): Legal 20.0%, Causal 0.0%
- **Adversarial Exploit** (n=4): Legal 25.0%, Causal 100.0%
- **Deceptive Marketing** (n=5): Legal 40.0%, Causal 0.0%

### The Causal vs. Legal Divergence

v0.4 continues to prove the core architectural thesis of CausalLayer: **causation ≠ legal responsibility**.

In categories like *Privacy Consent* and *Adversarial Exploit*, the causal axis scores 100% (correctly identifying the technical origin of the failure) while the legal axis scores 50% or 25% (struggling to apply the correct legal doctrine to that technical failure).

Carriers need both views. The benchmark now rigorously grades both.

### Artefacts

- `calb2_v04.json`: The 137-case corpus with dual ground-truth.
- `calb2_v04_scenario_map.json`: The full v0.7 engine output for every case.
- `analysis/`: Charts and JSON findings.
- `anchors/`: The OpenTimestamps receipt proving the entire run was committed to the Bitcoin blockchain on 15 May 2026.
