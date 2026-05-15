# CausalLayer CALB-2 v0.8 Expansion Report

**Date:** 15 May 2026  
**Engine Version:** v1.2.0  
**Corpus Version:** v0.8.0 (250 cases)  

## Executive Summary

We successfully expanded the CALB-2 corpus from 202 to 250 cases, injecting 48 fresh, public, verifiable AI-incident cases. The expansion targeted previously underweight domains (aviation, automotive, government, hr_employment) and stress-tested the engine against new doctrine surfaces (defamation, copyright, and complex human-in-the-loop handovers).

Running the v1.2.0 engine blind over this expanded corpus revealed a stark but expected generalisation gap:
- **v0.7.2 baseline accuracy (n=202):** 91.6%
- **v0.8 fresh cases accuracy (n=48):** 62.5%
- **Overall v0.8 corpus accuracy (n=250):** 86.0%

This 37.5% miss rate on fresh data perfectly maps the attack surface for the v1.3 engine cycle.

## Key Failure Modes for v1.3 Scoping

The 18 misses on the fresh cases cluster into several distinct, addressable failure modes:

### 1. The "Fake Cases" Attorney Sanction Cluster (L7-201, L7-202, L7-203, L7-204, L7-205)
**The pattern:** Attorneys use ChatGPT or internal LLMs to draft briefs, submit hallucinated case citations to a court, and are sanctioned under Rule 11 or state equivalents.
**The engine failure:** The engine predicts `ai_provider` (Strict Product Liability) or `deployer` (Regulatory Action), but the ground truth is `human_operator` (the attorney who failed their non-delegable duty of candor to the court).
**v1.3 Fix:** The FRCP-11 doctrine needs to be expanded to catch these cases and route liability 100% to the `human_operator` when the failure is `hallucination_fabrication` in a `legal_services` domain.

### 2. Defamation by AI / Section 230 (L1-256, L7-251)
**The pattern:** Pro-se plaintiffs sue AI providers (OpenAI, Microsoft) because the LLM generated defamatory statements about them.
**The engine failure:** The engine predicts `ai_provider` (Strict Product Liability), but courts are routinely dismissing these under Section 230 or lack of publication, leaving the loss with the `affected_party` or `human_operator` (the prompter).
**v1.3 Fix:** Implement a dedicated Publisher Liability / Defamation doctrine that routes `defamation_by_ai` cases to `human_operator` or `affected_party` depending on the jurisdiction's Section 230 equivalent.

### 3. Aviation / Automotive Sensor Failures (L9-203, L9-205, L4-204)
**The pattern:** Complex sensor/autonomy failures (Boeing 737 MAX MCAS, Tesla Autopilot) where the NTSB/AAIB apportions blame to the manufacturer, but the engine misroutes.
**The engine failure:** The engine routes to `deployer` (the airline) or `ai_provider` incorrectly because the Level-2 Automation Handover doctrine isn't catching the specific `perception_sensor_failure` or the source types aren't matching the aviation safety board list.
**v1.3 Fix:** Broaden the Level-2 aviation branch to catch `perception_sensor_failure` and ensure NTSB/AAIB/KNKT reports trigger the correct 50/50 or provider-heavy apportionment.

### 4. Algorithmic Government Action (L8-201, L8-204)
**The pattern:** Government agencies deploy flawed algorithms (Robodebt, Allegheny Family Screening) and face regulatory or public inquiry.
**The engine failure:** The engine predicts `ai_provider` (Regulatory Action), but the ground truth is `deployer` (the government agency is held responsible for the administrative failure).
**v1.3 Fix:** The Government Administrative Liability doctrine needs to fire more reliably when `failure_category` is `algorithmic_government_action`, overriding the standard Regulatory Action rule.

## Cryptographic Anchor

The v0.8 run has been anchored to the Bitcoin blockchain via OpenTimestamps:
- **Date:** 2026-05-15
- **Merkle Root:** `8356b9f51ff9047e37963f9146f995d2987a6b5415c6e1bcca7a2e6278af941e`
- **Leaves:** 250
- **File:** `causallayer-anchor-log/anchors/2026-05-15-v1.2-calb2-v0.8.0.json(.ots)`

## Next Steps

1. Review this report and the attached CSV of the 18 misses.
2. Approve the v1.3 scoping (specifically the FRCP-11 and Defamation doctrine additions).
3. Initiate the v1.3 engine cycle.
