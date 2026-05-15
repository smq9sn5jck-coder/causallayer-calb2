# CALB-2 v0.9 Run — Summary

- Corpus: 280 cases (v0.8 baseline 250 + v0.9 fresh 30)
- Engine: v1.4.0 (extended_attribution sidecar shipped in v1.4)

## Headline numbers

| Slice | Top-1 (all) | Top-1 (hi-conf) |
| --- | --- | --- |
| Overall (n=280) | **247/280 = 88.2%** | **175/193 = 90.7%** |
| Baseline v0.8 (n=250) | 227/250 = 90.8% | 164/175 = 93.7% |
| Fresh v0.9 (n=30) | 20/30 = 66.7% | 11/18 = 61.1% |

## Reference: prior cycles

| Run | All | Hi-conf |
| --- | --- | --- |
| v1.2 on v0.7.2 (202) | 91.6% | 95.4% |
| v1.2 on v0.8 (250) | 86.0% | 88.6% |
| v1.3 on v0.8 (250) | 90.0% | 93.1% |
| v1.4 on v0.8 (250) | 90.8% | 93.7% |
| **v1.4 on v0.9 (280)** | **88.2%** | **90.7%** |

Blind-expansion delta (v1.4 v0.8 → v1.4 v0.9): **-2.6pp all / -3.0pp hi-conf**.
