# CALB-2 v0.8 Expansion: Failure Mode Analysis

**New cases added:** 48
**New cases missed by v1.2.0:** 18 (37.5% miss rate on fresh data)

## Misses by Doctrine

### Regulatory Action / Statutory Liability (Deployer) (n=5)
- **L2-206** South Korean PIPC Fine to Meta for Unlawful Targeted-Advertising AI Inferences  
  *Predicted:* deployer | *GT:* ai_provider | *FC:* privacy_consent  
- **L4-205** Waymo NHTSA Recall 24E-013 for Software Collision Avoidance Issue  
  *Predicted:* deployer | *GT:* ai_provider | *FC:* perception_failure  
- **L7-204** People v. Zachariah C. Crabill  
  *Predicted:* deployer | *GT:* human_operator | *FC:* hallucination_fabrication  
- **L9-203** Ethiopian Airlines Flight 302 Boeing 737 MAX Crash  
  *Predicted:* deployer | *GT:* ai_provider | *FC:* perception_sensor_failure  
- **L9-205** KNKT Investigation on Sriwijaya Air Flight SJ-182 Boeing 737-500 Autothrottle Anomaly  
  *Predicted:* deployer | *GT:* human_operator | *FC:* perception_sensor_failure  

### Regulatory Action / Statutory Liability (Provider) (n=5)
- **L2-203** AEPD Spain Ban on Worldcoin Biometric Iris Scanning  
  *Predicted:* ai_provider | *GT:* deployer | *FC:* privacy_consent  
- **L4-204** NTSB Investigation on Tesla Autopilot Williston Florida Fatal Crash  
  *Predicted:* ai_provider | *GT:* external_actor | *FC:* perception_sensor_failure  
- **L6-202** Italian AGCM fine against TikTok for French scar challenge  
  *Predicted:* ai_provider | *GT:* deployer | *FC:* oversight_failure  
- **L8-201** Robodebt Royal Commission Final Report  
  *Predicted:* ai_provider | *GT:* deployer | *FC:* algorithmic_government_action  
- **L8-204** DOJ Investigation into Allegheny County Family Screening Tool  
  *Predicted:* ai_provider | *GT:* deployer | *FC:* bias_discrimination  

### Strict Product Liability / Design Defect (n=3)
- **L7-201** Mata v. Avianca Inc.  
  *Predicted:* ai_provider | *GT:* human_operator | *FC:* hallucination_fabrication  
- **L7-202** Park v. Kim, 91 F.4th 610 (2d Cir. 2024)  
  *Predicted:* ai_provider | *GT:* human_operator | *FC:* hallucination_fabrication  
- **L7-205** DPP v. AB (Australia) - Victorian solicitor referred to legal-services board after AI-generated case citations submitted in family-court matter  
  *Predicted:* ai_provider | *GT:* human_operator | *FC:* hallucination_fabrication  

### FTC Section 5 Deceptive Marketing / Provider (n=2)
- **L5-201** Massachusetts AG Settlement with Joshua Hyman / Sumiyo Inc. over AI Lawyer Marketing  
  *Predicted:* ai_provider | *GT:* deployer | *FC:* deceptive_marketing  
- **L5-204** FTC v. CRI Genetics (2023)  
  *Predicted:* ai_provider | *GT:* deployer | *FC:* deceptive_marketing  

### Strict Product Liability / Vertically-Integrated Producer (AI-as-Product) (n=2)
- **L1-256** Battle v. Microsoft Corp.  
  *Predicted:* ai_provider | *GT:* external_actor | *FC:* defamation_by_ai  
- **L7-251** Walters v. OpenAI L.L.C.  
  *Predicted:* ai_provider | *GT:* human_operator | *FC:* defamation_by_ai  

### Negligent Operations / In-House Algorithmic Failure (n=1)
- **L7-203** Wadsworth v. Walmart Inc. (D. Wyo. Feb 2025)  
  *Predicted:* deployer | *GT:* human_operator | *FC:* hallucination_fabrication  
