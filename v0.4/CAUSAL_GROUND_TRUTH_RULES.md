# CALB-2 Causal Ground-Truth Derivation Rules (v0.3)

## Purpose

CALB-2 v0.1 and v0.2 grade engine output against a single ground-truth column
(`liability_allocation`) populated from court rulings and regulator orders.
That column captures **legal responsibility** — who the law holds responsible
once the dispute is adjudicated.

The CausalLayer engine produces **two** axes of attribution: causal and legal.
Grading both axes against a legal-only ground-truth column understates the
causal axis whenever causation and legal responsibility diverge (e.g., FRCP
Rule 11 cases where the AI hallucinated but the court holds the lawyer fully
responsible).

CALB-2 v0.3 introduces a second ground-truth column, `causal_allocation`, that
captures the technical/causal pathway: whose system or action originated the
failure, irrespective of who bears legal responsibility for it. This document
describes the deterministic rules used to populate that column from the
existing case data.

## Ground rules

1. **No subjective re-interpretation of facts.** Causal allocations are derived
   strictly from `failure_category`, `telemetry`, `system_architecture`, and
   `incident_description` — fields already present in the corpus.
2. **Vertical integration is the dominant disambiguator.** When a deployer
   built or substantially configured the AI system itself, the deployer plays
   both the producer and operator roles in the causal chain.
3. **Confidence is recorded.** Each allocation carries a `causal_confidence`
   field of `high` or `medium`. Cases where automated rules cannot decide are
   flagged `manual_review`.
4. **Reproducibility.** Re-running `enrich_causal_ground_truth.py` against the
   v0.1 corpus produces byte-identical v0.3 causal columns. The script and
   this rules document together constitute the complete derivation.

## Helper: vertical integration test

A deployer is treated as **vertically integrated** (i.e., also the producer)
when any of the following holds:

- `telemetry.deployer_org` and `telemetry.model_provider` are equal (case-insensitive)
- `model_provider` is missing or one of `unknown / n/a / none / implied / unidentified`
  while `deployer_org` is named
- The `deployer_org` and `model_provider` strings share at least one token of
  length ≥ 4 (e.g., "Cruise LLC" / "Cruise" → integrated)

## Rule table

| Rule | Failure category | Vertically integrated? | Causal allocation | Confidence |
|---|---|---|---|---|
| C1a | hallucination_fabrication, specification_oversight | No | ai_provider 80, human_operator 20 | high |
| C1b | hallucination_fabrication, specification_oversight | Yes | deployer 100 | high |
| C2a | bias_discrimination, training_data_bias | Yes | deployer 100 | high |
| C2b | bias_discrimination, training_data_bias | No | ai_provider 70, deployer 30 | medium |
| C3a | perception_sensor_failure, perception_failure | Yes | deployer 100 | high |
| C3b | perception_sensor_failure, perception_failure | No | ai_provider 70, deployer 30 | medium |
| C4a | autonomy_handover | Yes | deployer 60, human_operator 40 | medium |
| C4b | autonomy_handover | No | ai_provider 50, deployer 10, human_operator 40 | medium |
| C5  | privacy_consent | (any) | ai_provider 20, deployer 80 | high |
| C6  | intellectual_property | (any) | ai_provider 80, data_provider 20 | medium |
| C7  | deceptive_marketing | (any) | deployer 100 | high |
| C8  | algorithmic_government_action | (any) | ai_provider 30, deployer 70 | medium |
| C9  | pipeline_data_quality | (any) | ai_provider 20, deployer 20, data_provider 60 | medium |
| C10 | adversarial_input, prompt_injection | (any) | ai_provider 70, deployer 30 | medium |
| C11 | deployer_misconfiguration | (any) | deployer 100 | high |
| C12 | data_provider_failure | (any) | data_provider 100 | high |

## Discussion of edge cases

**Lawyer-hallucination (C1a, 57 cases).** The model produced false output;
the human operator failed to validate. Causally, the AI is the originator;
the human is a contributor for non-validation. Note this is the *opposite* of
the legal allocation, which puts 100% on the human under FRCP Rule 11. The
divergence is the central finding of CALB-2 v0.1.

**Vertically-integrated bias (C2a, 2 cases).** When the deployer trained or
configured the discriminatory system itself (iTutorGroup), the deployer is the
causal producer.

**Vertically-integrated perception (C3a, 2 cases).** When the deployer built
the autonomous vehicle system itself (Cruise), the deployer is the causal
producer.

**Deceptive marketing (C7, 5 cases).** Marketing communications are a
deployer-side action; even if the AI's output triggered the dispute (e.g., Air
Canada chatbot), the marketing decision to deploy the chatbot as a customer
agent without policy synchronisation is the proximate causal failure.

## Out of scope for v0.3

- Cases marked `manual_review` (zero in v0.3, but reserved for future expansion).
- Multi-pathway causation where two or more pathways contribute roughly
  equally and the rules above resolve to one. Future v0.4 may introduce
  case-by-case adjudicated causal allocations for such cases.

## How this is used

- The CALB-2 v0.3 corpus is graded on two columns:
  - `liability_allocation` against the engine's `legal_attribution` axis
  - `causal_allocation` against the engine's `causal_attribution` axis
- The CausalLayer v0.7 engine is held to the per-axis ground truth, not the
  composite. This is the only fair test of dual-axis architecture.

## Provenance

This document is part of CALB-2 v0.3 and is published under CC0 1.0 Universal.
The deterministic enricher is in `enrich_causal_ground_truth.py`. Re-running
it is sufficient to reproduce the v0.3 causal column from the v0.1 corpus.
