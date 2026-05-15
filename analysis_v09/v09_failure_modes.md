# CALB-2 v0.9 — Failure-Mode Taxonomy

Total misses (n=280): **33**  
Fresh-case misses (n=30): **10** (33.3% miss rate)  
Baseline regressions (n=250): **23** (9.2% miss rate)  

## Confusion pairs — overall (predicted → GT)

| Predicted | GT | Count | Notes |
| --- | --- | --- | --- |
| ai_provider | deployer | 15 | 6 fresh |
| deployer | ai_provider | 4 | 1 fresh |
| ai_provider | human_operator | 4 | 1 fresh |
| deployer | human_operator | 3 | all baseline |
| human_operator | deployer | 2 | all baseline |
| deployer | data_provider | 2 | all baseline |
| external_actor | ai_provider | 1 | all baseline |
| ai_provider | affected_party | 1 | 1 fresh |
| ai_provider | regulator | 1 | 1 fresh |

## Fresh-case misses — case detail

| Case | Title | Domain | Pred → GT | Doctrine fired |
| --- | --- | --- | --- | --- |
| `L1-304` | Concord Music Group, Inc. v. Anthropic PBC | media | ai_provider → affected_party | Training-Data IP Infringement / Copyright Liability |
| `L11-301` | In the Matter of Delphia (USA) Inc., Investment Adviser | financial_services | ai_provider → deployer | FTC Section 5 Deceptive Marketing / Provider |
| `L11-302` | In the Matter of Global Predictions, Inc., Release No.  | financial_services | ai_provider → deployer | FTC Section 5 Deceptive Marketing / Provider |
| `L2-304` | In the Matter of Cleo AI, Inc., FTC Matter No. 2423004 | financial_services | ai_provider → deployer | FTC Section 5 Deceptive Marketing / Provider |
| `L4-302` | NHTSA Announces Consent Order with Cruise After Company | automotive | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L4-305` | Parts and Accessories Necessary for Safe Operation; App | automotive | ai_provider → regulator | Strict Product Liability / Vertically-Integrated Produc |
| `L5-301` | SeniorLife Technologies, Inc. - 707021 - 08/21/2025 | healthcare | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L6-302` | Commission preliminarily finds TikTok's addictive desig | media | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L6-304` | Investigation into Amazon's Marketplace | consumer_retail | deployer → ai_provider | Regulatory Action / Statutory Liability (Deployer) |
| `L9-302` | Electric Vehicle Run-Off-Road Crash and Postcrash Fire, | automotive | ai_provider → human_operator | Regulatory Action / Statutory Liability (Provider) |

## Baseline regressions — case detail

| Case | Title | Pred → GT | Doctrine fired |
| --- | --- | --- | --- |
| `L11-901` | Wong et al. Validation of Epic Sepsis Model | ai_provider → deployer | Strict Product Liability / Design Defect |
| `L11-903` | Roberts et al. on Spurious Correlations in COVID-19 Che | deployer → data_provider | Strict Product Liability / Vertically-Integrated Produc |
| `L2-005` | State v. Loomis | human_operator → deployer | Judicial Discretion / Decision-Maker Non-Delegability |
| `L2-116` | State v. Loomis | deployer → human_operator | Government Administrative Liability / Non-Delegable Dut |
| `L2-203` | AEPD Spain Ban on Worldcoin Biometric Iris Scanning | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L2-206` | South Korean PIPC Fine to Meta for Unlawful Targeted-Ad | deployer → ai_provider | Regulatory Action / Statutory Liability (Deployer) |
| `L2-901` | NY DFS Investigation on Apple Card and Goldman Sachs | deployer → ai_provider | Negligent Operations / In-House Algorithmic Failure |
| `L2-903` | New York State Department of Financial Services Action  | deployer → ai_provider | Regulatory Action / Statutory Liability (Deployer) |
| `L2-909` | Crawford and Paglen v. ImageNet | deployer → data_provider | Strict Product Liability / Vertically-Integrated Produc |
| `L2-912` | State v. Pickett COMPAS challenge | human_operator → deployer | Judicial Discretion / Decision-Maker Non-Delegability |
| `L3-901` | Kevin Liu v. Microsoft Corporation | ai_provider → human_operator | Strict Product Liability / Design Defect |
| `L3-903` | Samsung bans ChatGPT after internal data leak | ai_provider → human_operator | Strict Product Liability / Design Defect |
| `L4-901` | AWS S3 us-east-1 Outage Cascading Failures | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L5-201` | Massachusetts AG Settlement with Joshua Hyman / Sumiyo  | ai_provider → deployer | FTC Section 5 Deceptive Marketing / Provider |
| `L5-204` | FTC v. CRI Genetics (2023) | ai_provider → deployer | FTC Section 5 Deceptive Marketing / Provider |
| `L5-903` | FTC Action on Ascend Ecom | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L6-202` | Italian AGCM fine against TikTok for French scar challe | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L6-901` | Hamburg DPA v. H&M Hennes & Mauritz Online Shop A.B. &  | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L6-906` | CNIL v. Doctissimo | ai_provider → deployer | Regulatory Action / Statutory Liability (Provider) |
| `L7-001` | Walters v. OpenAI, L.L.C. | deployer → human_operator | Negligent Deployment / Constructive Knowledge |
| `L7-201` | Mata v. Avianca Inc. | deployer → human_operator | FRCP Rule 11 / Professional Non-Delegable Duty (joint s |
| `L7-902` | Battle v. Microsoft Corporation | external_actor → ai_provider | Generative-AI Defamation / No Publisher Liability |
| `L9-901` | NTSB Investigation on Tesla Autopilot Joshua Brown Fata | ai_provider → human_operator | Regulatory Action / Statutory Liability (Provider) |
