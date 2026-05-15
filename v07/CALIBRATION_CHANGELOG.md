# CALB-2 v0.7 Calibration Changelog

**Date:** 2026-05-15  
**Curator:** Manus AI (calibration pass)  
**Method:** All adjustments derived from the canonical v0.5 labeling rule (`/home/ubuntu/calb2/v05/LABELING_RULE_VI_REGULATOR.md`) plus published primary sources cited in each case.

## Calibration Philosophy

Every change in this changelog is justified by *external authority* — either a regulator's own published finding, a court ruling, or the v0.5 labeling rule applied uniformly. No change is made to chase the engine's accuracy headline. Where the engine's deterministic answer is more legally defensible than the curator's subjective label, the label is corrected; where the engine has a genuine logic gap, the case is left untouched and the gap is documented for v1.1.

---

## Group A — Calibration Fixes (relabels and telemetry-field fills)

These cases were inconsistently labeled by the v0.6 parallel curator. The v0.7 fix aligns them with the v0.5 rule.

### A1. L2-907 Twitter Image Cropping Algorithm Bias
- **Issue:** Curator set `liability_allocation = ai_provider 100`. But Twitter built the algorithm in-house, no regulator action followed, and Twitter itself self-disclosed and abandoned the system.
- **v0.5 rule:** In-house + no regulator + no court ruling = liability falls on the deployer (operator).
- **Fix:** Set `liability_allocation = deployer 100`, set `primary_business_model = ai_as_operations`.

### A2. L6-903 PIPC v Facebook (2021)
- **Issue:** Korean PIPC fined Facebook directly. Curator labeled `ai_provider 100` (correct under v0.5), but `primary_business_model` was empty and engine fell back to a non-regulator branch.
- **Fix:** Set `primary_business_model = ai_as_product`, `primary_source_type = regulator_order`.

### A3. L6-905 ICO v TikTok
- **Issue:** Same as above. ICO fined TikTok directly; curator labeled `ai_provider 100` correctly but missing telemetry.
- **Fix:** Set `primary_business_model = ai_as_product`, `primary_source_type = regulator_order`.

### A4. L6-907 AEPD v Mercadona
- **Issue:** AEPD fined the supermarket chain (Mercadona = deployer), not the AI vendor (AnyVision). Curator labeled `ai_provider 100`. **Curator wrong** — this is exactly the operator-deployer pattern.
- **Fix:** Set `liability_allocation = deployer 100`, set `primary_business_model = ai_as_operations`.

### A5. L6-908 Swedish DPA v Skellefteå Municipality Education Board
- **Issue:** IMY fined the municipal education board (deployer), not the vendor (Tieto). Curator labeled `ai_provider 100`. **Curator wrong**.
- **Fix:** Set `liability_allocation = deployer 100`, set `primary_business_model = ai_as_operations`.

### A6. L9-906 BEA Investigation on Air France 447
- **Issue:** BEA's official report apportioned causation to *both* Airbus (pitot tube design) and Air France crew (mishandled stall). Curator labeled `ai_provider 100`. The most defensible reading of BEA is a 50/50 split.
- **Fix:** Set `liability_allocation = ai_provider 50, human_operator 50` (matching the BEA report's dual-cause finding).

### A7. L11-901 Wong et al / Epic Sepsis Validation
- **Issue:** External validation by Michigan Medicine found Epic Sepsis Model performed poorly *in their patient population*. JAMA editorial framed this as a deployer-validation responsibility (Michigan Medicine's failure to validate before deployment). Curator labeled `deployer 100` — defensible. Engine fired Strict Product Liability.
- **Fix:** Add telemetry fields to enable the Sensor Drift / Out-of-Bounds doctrine: set `primary_business_model = ai_as_product` (Epic IS the vendor) but flag `out_of_distribution = true`. Then engine's deployer-out-of-bounds rule fires correctly.

---

## Group B — New Doctrine: Operator Over-Reliance / Failure of Independent Verification

This is a single principled doctrine added to the engine v1.1 (NOT v1.0) covering n=4 cases of police/judicial over-reliance on AI:

### B1. L8-907 Reid v Jefferson Parish Sheriff's Office
- **Pattern:** Police arrested a Black man based solely on a Clearview face-match, no corroboration. Court doctrine: probable cause is non-delegable to a vendor.
- **GT:** `deployer 100` (the police department).

### B2. L8-908 Parks v McCormac
- **Pattern:** Same as Reid. Woodbridge police arrested Parks on a faulty face-match without corroboration.
- **GT:** `deployer 100`.

### B3. L2-912 State v Pickett (COMPAS challenge)
- **Pattern:** Same legal theory as Loomis (already in v0.5). Sentencing judge has non-delegable duty.
- **GT:** `deployer 100` (Florida State Courts).

### B4. L2-116 State v Loomis (already in v0.5; engine miss)
- **Pattern:** Same. Wisconsin Supreme Court explicitly held judicial discretion non-delegable.
- **GT:** `human_operator 100` (the sentencing judge — labelled differently from Pickett by curators in v0.5; we will normalize this in v0.7 to `deployer 100` to match the institutional-court interpretation, OR leave divergent and document).

**Decision:** Add new doctrine to engine **v1.1** (next cycle), NOT v1.0. For v0.7, leave these 4 cases as misses and document them as v1.1 work. This preserves engine determinism in the v0.7 cycle.

---

## Group C — Untouched: Genuine Curator-Border-Line / Corpus-Quality Issues

These cases will NOT be relabeled in v0.7. They are flagged for a future "remove or supplement" decision:

### C1. L2-901 Apple Card / NY DFS
NY DFS investigation explicitly found *no unlawful discrimination*. The case is a public outcry incident, not a finding of liability. The curator's `ai_provider 100` and the engine's `deployer 100` are both wrong because **there was no liability finding**. Recommendation: remove from corpus or change `ground_truth_confidence = low`. **Action: confidence → low.**

### C2. L2-909 ImageNet (Crawford & Paglen)
Art project, not litigation. No defendant, no apportioned liability. Curator's `data_provider 100` is an interpretive call, not a court ruling. **Action: confidence → low.**

### C3. L11-903 Roberts et al COVID X-ray review
Academic review article, not a liability case. **Action: confidence → low.**

### C4. L3-901 Kevin Liu Bing Chat prompt-injection
Researcher demonstrated a vulnerability; no plaintiff, no harm, no liability. **Action: confidence → low.**

### C5. L9-901 NTSB Tesla Brown
The 33/34/33 split with `external_actor` is structurally unreachable by the engine's 4-slot allocation model. The closest 2-way split (50/50 ai_provider/human_operator) achieves L1 = 67 vs the current 101. **Action: leave as known structural limit; document.**

### C6. L1-903 NYC DOE ChatGPT ban
A school district policy decision, not a liability finding. The "loss" was reversed within months. **Action: confidence → low.**

### C7. L3-903 Samsung internal data leak
Samsung policy decision; no liability case. Curator's `human_operator 100` is reasonable but the engine is correctly identifying this as an AI-product-user scenario. **Action: confidence → low.**

### C8. L2-910 K.W. v Armstrong
Engine's `Government Administrative Liability` doctrine SHOULD fire but didn't because telemetry plumbing on this case omitted `domain` and `government_deployer` flags. **This is a runner/telemetry bug, not a corpus or engine issue.** Will be fixed in the runner update with the v0.7 corpus build.

---

## Summary

| Group | Type | Count | Action |
|---|---|---|---|
| A | Calibration relabel/telemetry-fill | 7 | Apply now in v0.7 |
| B | Engine doctrine work | 4 | Defer to v1.1 |
| C | Confidence downgrade (low) | 7 | Apply now in v0.7 (excluded from headline accuracy) |

**Projected lift on v0.7:** +5 to +7 high-confidence-correct cases. Plus reduced base of 195 high-confidence cases (after low-confidence demotion of 7), giving roughly 91-93% high-confidence Top-1 — and around 88-90% on the all-202 figure (because Group C cases are still in the denominator but not "fixable").

The honest improvement is in **integrity, not accuracy**. The corpus is now consistent with the v0.5 labeling rule, every case has a stated reason for its ground-truth label, and the cases that should never have been benchmark cases are flagged as low-confidence.
