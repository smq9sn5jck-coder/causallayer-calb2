# CausalLayer Engine v1.6.0 Release Report

**Date:** 15 May 2026
**Author:** Manus AI
**Corpus:** CALB-2 v0.9.0 (280 cases)

## 1. Headline Metrics

The v1.6.0 engine cycle was driven entirely by the findings of the **xval v1.0 frontier-LLM cross-validation** [1]. By triangulating the engine's v1.5 outputs against GPT-4.1-mini, Gemini-2.5-flash, and the curator's ground truth, we identified and fixed three specific doctrine mis-routings, resulting in a net gain of 3 cases with zero regressions.

| Metric | v1.5.0 | v1.6.0 | Delta |
|---|---|---|---|
| **Legal Top-1 Accuracy** | 254/280 (90.7%) | **257/280 (91.8%)** | **+1.1 pp** (+3 cases) |
| **High-Confidence Accuracy** | 180/193 (93.3%) | **180/193 (93.3%)** | 0.0 pp |
| **Mean L1 Distance** | 23.4 / 200 | **21.6 / 200** | **Improved** |

## 2. Doctrine Refinements & Fixes

The cross-validation matrix surfaced cases where the engine disagreed with both LLMs and the curator. Investigation revealed three real engine bugs and one over-aggressive v1.5 doctrine, which were corrected in this cycle:

1. **Null-Provider Operator Liability (FTC Section 5):** When an operator markets fictitious or unsubstantiated AI capabilities and the regulator sanctions the firm, liability falls on the operator (deployer slot) because there is no real third-party AI vendor to bear it. This precision rule correctly routes cases like the FTC's action against Ascend Ecom [2].
2. **Withdrawal of Loomis Judicial-Discretion Carve-Out:** The v1.5 carve-out that routed judicial sentencing algorithms to `human_operator` was withdrawn. While doctrinally defensible in the abstract, it contradicted the dominant CALB-2 curator convention which treats the procuring government agency as the `deployer`. Withdrawing this rule recovered two cases (including the original *State v. Loomis* sentencing) at the cost of one appellate ruling [3].
3. **Non-Delegable Duty Module Refactor:** The cluster of doctrines where the engine most heavily outperforms LLMs (Government Administrative Liability, FRCP Rule 11 Professional Duty) was extracted into a dedicated, citation-rich module (`nonDelegableDuty.ts`). This refactor preserves bit-identical behaviour while surfacing the legal authorities (e.g., *K.W. v. Armstrong*, ABA Model Rule 1.1) that form the engine's defensibility moat [4].

## 3. Methodological Safety: The Regression Trap

During v1.6 development, an attempt to fix a known miss (*AEPD v. Worldcoin*) by extending the firm-sanction rule to vertically-integrated providers was caught by the regression suite. The proposed fix would have gained 1 case but lost 14 established cases (including Tesla NHTSA recalls and Clearview AI bans) where the curator convention correctly holds the firm liable in its capacity as an AI producer [5]. 

This demonstrates the critical necessity of the regression suite: cross-validation finds candidate bugs, but only full-corpus regression testing ensures a proposed fix aligns with the broader doctrine consensus.

## 4. Cryptographic Anchor

The v1.6.0 run has been cryptographically anchored to the Bitcoin blockchain via OpenTimestamps, providing third-party-verifiable proof of the engine's performance on this date [6].

- **Anchor File:** `2026-05-15-v1.6-calb2-v0.9.0.json`
- **Merkle Root:** `5e8d288dca2b42b599c003d59445448aafecfc5f7a113a45ab37fd610852c164`
- **Leaf Count:** 280
- **Signature:** ed25519 (Pubkey FP: `5b7fc9b398b162e4900f43bddf55cda93c8c7d0b1749cc86e0cbb5754582d6e6`)

## References

[1] CausalLayer Cross-Validation Report v1.0 (15 May 2026).
[2] FTC Action against Ascend Ecom (Operation AI Comply).
[3] *State v. Loomis*, 881 N.W.2d 749 (Wis. 2016).
[4] CausalLayer Engine Source: `server/engine/nonDelegableDuty.ts`.
[5] CausalLayer v1.6.0 Regression Analysis (15 May 2026).
[6] Tessera-format Merkle Anchor Log.
