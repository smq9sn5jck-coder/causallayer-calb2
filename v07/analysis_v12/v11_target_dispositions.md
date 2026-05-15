## v1.1 hi-conf miss disposition under v1.2

| Case | Plan | v1.2 result | Doctrine fired |
|---|---|---|---|
| L2-016 | Calibration + engine (top-level citation, in-house, stop-words) | ✓ FIXED | `Regulatory Action / Statutory Liability (Provider)` |
| L5-002 | Engine fix (FRCP-11 guard for regulator sources) | ✓ FIXED | `FTC Section 5 Deceptive Marketing / Provider` |
| L5-104 | Engine fix (tightened co-respondent) + corpus citation correction | ✓ FIXED | `Regulatory Action / Statutory Liability (Deployer)` |
| L6-903 | Engine fix (in-house provider detection) | ✓ FIXED | `Regulatory Action / Statutory Liability (Provider)` |
| L6-905 | Engine fix (in-house provider detection) | ✓ FIXED | `Regulatory Action / Statutory Liability (Provider)` |
| L9-906 | Engine fix (BEA aviation Level-2 branch) | ✓ FIXED | `Level-2 Automation / Safety-Board Fatal Investigation Apportionment` |
| L7-001 | Accept as noise (n=1 publisher liability) | ✗ STILL MISS | `Negligent Deployment / Constructive Knowledge` |
| L2-116 | Accept as noise (curator inconsistency with State v Pickett) | ✗ STILL MISS | `Government Administrative Liability / Non-Delegable Duty` |

**Resolved: 6/8 targeted hi-conf misses (the remaining 2 are documented noise, not engine bugs).**
