# CALB-2 v0.7.2 / Engine v1.2.0 Run Summary

Total cases : **202**  
Legal Top-1 (all)        : **185/202 = 91.6%**  
Legal Top-1 (high-conf)  : **144/151 = 95.4%**  
Causal Top-1 (all)       : 119/202 = 58.9%  

## Comparison vs v1.1

| Metric | v1.1 (CALB-2 v0.7) | v1.2 (CALB-2 v0.7.2) | Δ |
|---|---|---|---|
| Legal Top-1 (all)         | 91.6% (185/202) | 91.6% (185/202) | -0.0pp |
| Legal Top-1 (high-conf)   | 94.7% (143/151) | 95.4% (144/151) | +0.7pp |

## High-confidence legal misses

- **L2-116** State v. Loomis  
  doctrine: `Government Administrative Liability / Non-Delegable Duty`  
  predicted=deployer, gt=human_operator, L1=200  
- **L4-901** AWS S3 us-east-1 Outage Cascading Failures  
  doctrine: `Regulatory Action / Statutory Liability (Provider)`  
  predicted=ai_provider, gt=deployer, L1=200  
- **L5-903** FTC Action on Ascend Ecom  
  doctrine: `Regulatory Action / Statutory Liability (Provider)`  
  predicted=ai_provider, gt=deployer, L1=200  
- **L6-901** Hamburg DPA v. H&M Hennes & Mauritz Online Shop A.B. & Co KG  
  doctrine: `Regulatory Action / Statutory Liability (Provider)`  
  predicted=ai_provider, gt=deployer, L1=200  
- **L6-906** CNIL v. Doctissimo  
  doctrine: `Regulatory Action / Statutory Liability (Provider)`  
  predicted=ai_provider, gt=deployer, L1=200  
- **L7-001** Walters v. OpenAI, L.L.C.  
  doctrine: `Negligent Deployment / Constructive Knowledge`  
  predicted=deployer, gt=human_operator, L1=200  
- **L8-903** Dutch Data Protection Authority v. Tax and Customs Administration  
  doctrine: `Regulatory Action / Statutory Liability (Provider)`  
  predicted=ai_provider, gt=deployer, L1=200  

## All legal misses (n=17)

| Case | Conf | Domain | Doctrine | Predicted | GT | L1 |
|---|---|---|---|---|---|---|
| L11-901 | low | healthcare | `Strict Product Liability / Design Defect` | ai_provider | deployer | 200 |
| L11-903 | low | healthcare | `Strict Product Liability / Vertically-Integrated Producer` | deployer | data_provider | 200 |
| L2-005 | medium | criminal_justice | `Judicial Discretion / Decision-Maker Non-Delegability` | human_operator | deployer | 200 |
| L2-116 | high | criminal_justice | `Government Administrative Liability / Non-Delegable Duty` | deployer | human_operator | 200 |
| L2-901 | low | financial_services | `Negligent Operations / In-House Algorithmic Failure` | deployer | ai_provider | 200 |
| L2-903 | medium | healthcare | `Regulatory Action / Statutory Liability (Deployer)` | deployer | ai_provider | 200 |
| L2-909 | low | other | `Strict Product Liability / Vertically-Integrated Producer` | deployer | data_provider | 200 |
| L2-912 | low | criminal_justice | `Judicial Discretion / Decision-Maker Non-Delegability` | human_operator | deployer | 200 |
| L3-901 | low | other | `Strict Product Liability / Design Defect` | ai_provider | human_operator | 200 |
| L3-903 | low | other | `Strict Product Liability / Design Defect` | ai_provider | human_operator | 200 |
| L4-901 | high | other | `Regulatory Action / Statutory Liability (Provider)` | ai_provider | deployer | 200 |
| L5-903 | high | consumer_retail | `Regulatory Action / Statutory Liability (Provider)` | ai_provider | deployer | 200 |
| L6-901 | high | hr_employment | `Regulatory Action / Statutory Liability (Provider)` | ai_provider | deployer | 200 |
| L6-906 | high | media | `Regulatory Action / Statutory Liability (Provider)` | ai_provider | deployer | 200 |
| L7-001 | high | media | `Negligent Deployment / Constructive Knowledge` | deployer | human_operator | 200 |
| L8-903 | high | government | `Regulatory Action / Statutory Liability (Provider)` | ai_provider | deployer | 200 |
| L9-901 | low | automotive | `Regulatory Action / Statutory Liability (Provider)` | ai_provider | human_operator | 101 |

## Per-doctrine accuracy

| Doctrine | Hits/Total | Acc |
|---|---|---|
| FRCP Rule 11 / Professional Non-Delegable Duty | 68/68 | 100.0% |
| Regulatory Action / Statutory Liability (Provider) | 22/28 | 78.6% |
| Regulatory Action / Statutory Liability (Deployer) | 23/24 | 95.8% |
| Government Administrative Liability / Non-Delegable Duty | 18/19 | 94.7% |
| FRCP Rule 11 / Professional Non-Delegable Duty (firm sanction) | 9/9 | 100.0% |
| Strict Product Liability / Design Defect | 5/8 | 62.5% |
| Negligent Deployment / Constructive Knowledge | 7/8 | 87.5% |
| Strict Product Liability / Vertically-Integrated Producer (AI-as-Product) | 8/8 | 100.0% |
| FTC Section 5 Deceptive Marketing / Provider | 7/7 | 100.0% |
| Negligent Operations / In-House Algorithmic Failure | 6/7 | 85.7% |
| Training-Data IP Infringement / Copyright Liability | 5/5 | 100.0% |
| Strict Product Liability / Vertically-Integrated Producer | 1/3 | 33.3% |
| Judicial Discretion / Decision-Maker Non-Delegability | 0/2 | 0.0% |
| Level-2 Automation Shared Liability | 1/1 | 100.0% |
| Level-2 Automation / Part 573 Manufacturer Recall Liability | 1/1 | 100.0% |
| FTC Section 5 Deceptive Marketing / Integrated Marketer | 1/1 | 100.0% |
| FTC Section 5 Deceptive Marketing / Integrated AI Producer | 1/1 | 100.0% |
| Regulatory Action / Joint Respondents Co-Liability | 1/1 | 100.0% |
| Level-2 Automation / Safety-Board Fatal Investigation Apportionment | 1/1 | 100.0% |

## Per-domain accuracy

| Domain | Hits/Total | Acc |
|---|---|---|
| legal_services | 79/79 | 100.0% |
| consumer_retail | 22/23 | 95.7% |
| media | 14/16 | 87.5% |
| government | 15/16 | 93.8% |
| other | 11/15 | 73.3% |
| criminal_justice | 11/14 | 78.6% |
| automotive | 9/10 | 90.0% |
| healthcare | 6/9 | 66.7% |
| hr_employment | 6/7 | 85.7% |
| financial_services | 6/7 | 85.7% |
| aviation | 3/3 | 100.0% |
| education | 3/3 | 100.0% |
