#!/usr/bin/env python3
"""Apply v0.7 calibration relabels and telemetry fills to build calb2_v07.json."""
import json
from pathlib import Path

CORPUS_IN = "/home/ubuntu/calb2/v06/calb2_v06.json"
CORPUS_OUT = "/home/ubuntu/calb2/v07/calb2_v07.json"
Path(CORPUS_OUT).parent.mkdir(parents=True, exist_ok=True)

with open(CORPUS_IN) as f:
    corpus = json.load(f)

# Group A fixes
for c in corpus["cases"]:
    cid = c["id"]
    
    # A1. L2-907 Twitter Image Cropping
    if cid == "L2-907":
        c["liability_allocation"] = {"ai_provider": 0, "deployer": 100, "human_operator": 0, "data_provider": 0, "regulator": 0, "external_actor": 0, "affected_party": 0}
        c["primary_business_model"] = "ai_as_operations"
        
    # A2. L6-903 PIPC v Facebook
    elif cid == "L6-903":
        c["primary_business_model"] = "ai_as_product"
        c["primary_source_type"] = "regulator_order"
        
    # A3. L6-905 ICO v TikTok
    elif cid == "L6-905":
        c["primary_business_model"] = "ai_as_product"
        c["primary_source_type"] = "regulator_order"
        
    # A4. L6-907 AEPD v Mercadona
    elif cid == "L6-907":
        c["liability_allocation"] = {"ai_provider": 0, "deployer": 100, "human_operator": 0, "data_provider": 0, "regulator": 0, "external_actor": 0, "affected_party": 0}
        c["primary_business_model"] = "ai_as_operations"
        
    # A5. L6-908 Swedish DPA v Skellefteå
    elif cid == "L6-908":
        c["liability_allocation"] = {"ai_provider": 0, "deployer": 100, "human_operator": 0, "data_provider": 0, "regulator": 0, "external_actor": 0, "affected_party": 0}
        c["primary_business_model"] = "ai_as_operations"
        
    # A6. L9-906 BEA Air France 447
    elif cid == "L9-906":
        c["liability_allocation"] = {"ai_provider": 50, "deployer": 0, "human_operator": 50, "data_provider": 0, "regulator": 0, "external_actor": 0, "affected_party": 0}
        
    # A7. L11-901 Epic Sepsis Validation
    elif cid == "L11-901":
        c["primary_business_model"] = "ai_as_product"
        if "telemetry_signals" not in c:
            c["telemetry_signals"] = {}
        c["telemetry_signals"]["out_of_distribution"] = True

    # C8. L2-910 K.W. v Armstrong (telemetry plumbing fix)
    elif cid == "L2-910":
        if "telemetry_signals" not in c:
            c["telemetry_signals"] = {}
        c["telemetry_signals"]["domain"] = "healthcare"
        c["telemetry_signals"]["government_deployer"] = True

    # Group C - Low confidence demotions
    elif cid in ["L2-901", "L2-909", "L11-903", "L3-901", "L9-901", "L1-903", "L3-903"]:
        c["ground_truth_confidence"] = "low"

corpus["version"] = "calb2_v0.7"
corpus["changelog"] = corpus.get("changelog", []) + [
    "v0.7: Calibration pass on v0.6 new cases. Applied v0.5 labeling rule deterministically to fix curator inconsistencies. Demoted 7 non-liability/academic cases to low confidence."
]

with open(CORPUS_OUT, "w") as f:
    json.dump(corpus, f, indent=2)

print(f"Built {CORPUS_OUT} with {len(corpus['cases'])} cases.")
