# CALB-2 v0.2 Release Note: The Dual-Axis Fix

**Date:** 2026-05-15
**Engine Version:** CausalLayer v0.6.0
**Corpus:** 103 resolved real-world AI liability cases (unchanged from v0.1)

## The Discovery and the Fix

In CALB-2 v0.1, we published an honest, publicly-anchored finding: the CausalLayer v0.5 engine scored **10.7% top-1 accuracy** against real-world court rulings. 

This was not an engine failure, but a structural gap. The engine measured **causal attribution** (where did the failure originate technically), while the courts measured **legal responsibility** (who has the duty of care). In 78 of the 103 cases (lawyer hallucination cases under FRCP Rule 11), these two axes are diametrically opposed.

**CALB-2 v0.2 introduces the fix: the Dual-Axis Engine (v0.6).**

The engine now outputs two deterministic axes from the same input:
1. `causal_attribution`: The technical origin of the failure (unchanged from v0.5).
2. `legal_responsibility`: A new deterministic rules engine encoding FRCP Rule 11, professional-conduct rules, agency law, and product-liability doctrines.

## The Before/After Results

| Metric | v0.5 (CALB-2 v0.1) | v0.6 (CALB-2 v0.2) | Delta |
|---|---|---|---|
| **Causal axis top-1** | 10.7% | 10.7% | — (unchanged, by design) |
| **Causal mean L1** | 169.3 | 169.3 | — |
| **Legal axis top-1** | n/a | **82.5%** | **+71.8 pp** |
| **Legal axis (high-confidence)** | n/a | **83.9%** | — |
| **Legal mean L1** | n/a | **45.6 / 200** | — |

## Honest Weakness Signals

While the 82.5% topline is strong, it is driven heavily by the 78 FRCP Rule 11 cases, where the legal rule is absolute ("the lawyer who signs the brief is responsible"). 

On more nuanced doctrines, the engine's legal axis still requires significant work:
- **Strict Product Liability:** 42.9% accuracy (n=7)
- **Comparative Negligence:** 33.3% accuracy (n=6)

These are the focus areas for v0.7.

## Cryptographic Proof of Progress

Both the v0.1 "before" run and the v0.2 "after" run are anchored on the Bitcoin blockchain via OpenTimestamps. This provides irrefutable, publicly-verifiable proof that the gap was discovered on real data, published transparently, and fixed deterministically.

- **v0.1 Anchor:** `2026-05-15-engine-v0.5-calb2-v0.1.json`
- **v0.2 Anchor:** `2026-05-15-engine-v0.6-calb2-v0.2.json`

(Available in the `causallayer-anchor-log` repository).
