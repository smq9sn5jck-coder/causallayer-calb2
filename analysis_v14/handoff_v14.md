# CausalLayer Engine v1.4.0 — Sidecar Architecture

## Overview
The v1.4.0 release introduces the **Extended Attribution Sidecar**, solving a structural limitation in the engine's type system without breaking backward compatibility for existing anchors, tests, or downstream modules.

Previously, the engine's `PartyAttribution` type was strictly limited to four canonical slots (`ai_provider`, `deployer`, `data_provider`, `human_operator`). Cases where ground truth assigned liability to an `external_actor` (e.g., a third-party driver failing to yield) or an `affected_party` (e.g., a pro-se plaintiff in a dismissed defamation suit) were structurally unscorable.

v1.4.0 adds an `extended_attribution` sidecar to the `LegalResponsibilityResult`. The runner's `topParty` and L1 distance functions now consult this sidecar first, while the canonical 4-slot attribution remains intact (all-zeros) to satisfy the type system and preserve the ledger schema.

## Benchmark Results (CALB-2 v0.8.0, 250 cases)
- **Legal Top-1 (all):** 227 / 250 = **90.8 %** (up from 90.0 % in v1.3 → **+0.8 pp**)
- **Legal Top-1 (high-confidence):** 164 / 175 = **93.7 %** (up from 93.1 % in v1.3 → **+0.6 pp**)
- **Regression suite:** 52 / 52 unit tests passing across v0.7 → v1.4.

## Unblocked Cases
The sidecar architecture immediately unblocked two structurally unscorable cases:
1. **L4-204 (NTSB Williston Tesla Crash):** The new *External Actor / Third-Party Causation* doctrine detects third-party fault (a truck crossing the path) and routes 100% to `external_actor`.
2. **L1-256 (Battle v. Microsoft):** The *Generative-AI Defamation / No Publisher Liability* doctrine now correctly routes dismissed pro-se claims to `external_actor` (the affected party) instead of forcing them into the `human_operator` slot.

## Cryptographic Anchor
- **Merkle root:** `7676fe80ff41f4652674dc827889f50f1c650da4e4791d430e5d095f2cd410c3`
- **Leaves:** 250
- **File:** `2026-05-15-v1.4-calb2-v0.8.0.json(.ots)`
