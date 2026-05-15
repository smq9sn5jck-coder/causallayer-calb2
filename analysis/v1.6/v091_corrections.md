# CALB-2 v0.9.1 Curator Drift Corrections

_Applied 2026-05-15T19:39:57.307827+00:00_

Source corpus: `/home/ubuntu/calb2/v09/calb2_v09.json` (v0.9.0, 280 cases)
Output corpus: `/home/ubuntu/calb2/v09/calb2_v091.json` (v0.9.1, 280 cases, sha256 `04cdf00c8f8e8e3ceb4ffeb2a1a42f7c113303b792988ccb159e30790777c7c2`)

Five HIGH-severity violations from `analysis/v1.6/drift_candidates_v1.csv` are resolved below.  Each correction includes the rule, the fix target, the doctrinal justification, and the before/after field values.  An audit-trail record is written into `case.curator_corrections[]` on each affected case.

## L5-903 — FTC Action on Ascend Ecom

- **Rule violated:** `R1_joint_sanction_must_show_in_2plus_slots`
- **Fix target:** `liability_allocation`
- **Resolution:** Reallocate to deployer=70, human_operator=30 to honor the joint sanction of corporate deployer + individual owners under FTC §5 / Standard Education Society common-control liability.

- **liability_allocation (before):** `{'deployer': 100}`
- **liability_allocation (after):**  `{'deployer': 70, 'human_operator': 30}`

## L7-201 — Mata v. Avianca, Inc.

- **Rule violated:** `R1_joint_sanction_must_show_in_2plus_slots`
- **Fix target:** `liability_allocation`
- **Resolution:** Reallocate to human_operator=80, deployer=20 to capture FRCP Rule 11(c)(1) joint sanction of attorneys + firm.

- **liability_allocation (before):** `{'human_operator': 100}`
- **liability_allocation (after):**  `{'deployer': 20, 'human_operator': 80}`

## L8-902 — Cahoo v. SAS Analytics Inc.

- **Rule violated:** `R1_joint_sanction_must_show_in_2plus_slots`
- **Fix target:** `liability_allocation`
- **Resolution:** Reallocate to deployer=70, ai_provider=30 to capture joint state-actor liability of Michigan UIA + SAS contractor (Lugar v. Edmondson Oil).

- **liability_allocation (before):** `{'deployer': 100}`
- **liability_allocation (after):**  `{'ai_provider': 30, 'deployer': 70}`

## L3-904 — US v. ANOM Distributors (Operation Trojan Shield)

- **Rule violated:** `R2_individual_sanction_must_include_human_operator`
- **Fix target:** `telemetry_signals.sanctioned_entity_role`
- **Resolution:** Change sanctioned_entity_role from 'individual' to 'firm'; the criminal defendants are external_actors in CALB taxonomy, not human_operators of the AI system.

- **telemetry_signals.sanctioned_entity_role (before):** `'individual'`
- **telemetry_signals.sanctioned_entity_role (after):**  `'firm'`

## L11-202 — In re Public Sector Algorithmic Audit (Strasbourg)

- **Rule violated:** `R6a_explicit_none_provider_cannot_have_ai_provider_liability`
- **Fix target:** `liability_allocation`
- **Resolution:** Zero ai_provider (model_provider='Unknown' is explicit-none); roll 20 points into deployer per CoE AI Framework Convention Art. 4–5 deployer-side duties.

- **liability_allocation (before):** `{'ai_provider': 20, 'deployer': 80}`
- **liability_allocation (after):**  `{'deployer': 100}`
