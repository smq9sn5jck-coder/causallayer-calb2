# CALB-2: The CausalLayer AI Liability Benchmark

CALB-2 is a public, CC0-licensed benchmark of resolved real-world AI liability incidents. It provides a ground-truth dataset for evaluating AI-liability attribution engines against actual court rulings, regulator findings, and settled claims.

## v0.1 Release (May 2026)

The v0.1 corpus contains **103 resolved cases** across 10 failure categories and 40+ jurisdictions. Every case includes a primary-source citation (court docket, regulator order, etc.) and a ground-truth liability allocation.

### The Causation vs. Responsibility Gap

The headline finding from the v0.1 benchmark run is the exposure of a systematic gap between **causal attribution** (where the failure originated technically) and **legal responsibility** (who bears the duty of care).

When tested against CALB-2 v0.1, the CausalLayer v0.5 engine achieved a **10.7% top-1 accuracy** against court outcomes. This is not a failure of the engine's causal logic, but a demonstration that courts and attribution engines are answering different questions.

For example, in 66 "lawyer hallucination" cases (e.g., *Mata v. Avianca*), the engine correctly identifies the AI provider as the causal origin of the hallucination. However, courts universally apply FRCP Rule 11 (or local equivalents) to assign 100% legal responsibility to the human operator who signed the filing.

This benchmark establishes that future attribution engines must output **both** causal attribution (for subrogation and technical root-cause) and legal responsibility apportionment (for defense and coverage).

### Repository Structure

- `v0.1/calb2_v01.json`: The full 103-case corpus with primary-source citations.
- `v0.1/engine_v0.5_results.json`: The scenario map showing the CausalLayer v0.5 engine's prediction vs. ground truth for every case.
- `v0.1/findings.json`: Structured metrics and gap analysis.
- `v0.1/charts/`: Visualizations of the accuracy, confusion matrix, and L1 distance distribution.

### License

The CALB-2 dataset is released under the Creative Commons Zero v1.0 Universal (CC0 1.0) Public Domain Dedication. You may copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

### Anchored Provenance

The entire v0.1 run (corpus + engine results) was anchored on the Bitcoin blockchain via OpenTimestamps on 2026-05-15. The cryptographic proof is available in the `causallayer-anchor-log` repository, proving that these results were recorded prior to any engine modifications.
