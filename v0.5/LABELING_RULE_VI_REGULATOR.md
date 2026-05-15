# CALB-2 v0.5 Labeling Rule: Vertically-Integrated Regulatory Actions

## The Problem

In CALB-2 v0.4, ground-truth liability allocation for vertically-integrated companies (where `model_provider == deployer_org`) sanctioned by a regulator was inconsistent. For example, Tesla (Autopilot) was labeled `ai_provider`, while Cruise (AV) was labeled `deployer`. This inconsistency created an artificial ceiling on engine accuracy, as no deterministic rule could resolve the ambiguity without overfitting.

## The Solution: `primary_business_model`

The inconsistency stems from a subjective judgment by corpus authors about the company's primary business. To make this deterministic, CALB-2 v0.5 introduces a new structured telemetry field: `primary_business_model`.

This field must be populated for all vertically-integrated cases, taking one of two values:

1. **`ai_as_product`**: The company's primary value proposition to the customer *is* the AI system itself. The customer is buying or licensing the AI capability.
   - *Examples:* Tesla (selling Autopilot as a feature), OpenAI (selling API access/ChatGPT), Clearview AI (selling face recognition), ROSS Intelligence (selling AI legal research).
2. **`ai_as_operations`**: The company's primary value proposition is a non-AI product or service, and the AI is used internally to operate, optimize, or deliver that service.
   - *Examples:* Cruise/Uber (selling transportation, using AI to drive), iTutorGroup (selling tutoring, using AI to hire), Knight Capital (market making, using AI to route orders), Amazon (selling retail goods, using AI for voice interface).

## The Labeling Rule

When a vertically-integrated company is subject to a regulatory action (`primary_source_type` is a regulator order, consent decree, etc.):

1. If `primary_business_model == "ai_as_product"`, the primary liability slot MUST be **`ai_provider`**.
   - *Rationale:* The regulator is sanctioning the entity in its capacity as the manufacturer/vendor of a defective or non-compliant AI product placed into commerce.
2. If `primary_business_model == "ai_as_operations"`, the primary liability slot MUST be **`deployer`**.
   - *Rationale:* The regulator is sanctioning the entity in its capacity as the operator of a business that negligently deployed automation in its operations.

*Exception:* If the case involves a professional non-delegable duty (e.g., a lawyer hallucinating citations under FRCP Rule 11), the liability slot remains `human_operator`, regardless of vertical integration.

## Audit and Relabeling

All 30 vertically-integrated regulatory cases in the CALB-2 v0.4 corpus (excluding the 5 FRCP Rule 11 cases) will be audited against this rule. Cases where the v0.4 ground truth conflicts with this rule will be relabeled in v0.5 to ensure consistency.
