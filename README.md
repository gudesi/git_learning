# ETF Rotation Strategy

## Overview

Multi-factor ETF rotation strategy for PTrade.

**Core idea:** Select the strongest ETFs from a diversified universe using:

* Multi-horizon risk-adjusted momentum
* Trend quality (slope × R²)
* Trend persistence
* Drawdown quality
* Trend stability
* Liquidity filters
* ATR-based risk parity sizing
* Portfolio risk budgeting
* Bull-market regime enhancement

**Design goals:**

* Participate in major market trends
* Avoid prolonged bear markets
* Rotate into stronger sectors
* Prefer smoother, persistent trends
* Penalize high-drawdown assets
* Maintain controlled portfolio volatility
* Adapt exposure according to market regimes

---

## Current Status

**Version:** P4-C1 Bull Allocation Audit (Completed)

**Completed Modules:**

* P0 Execution Layer Stabilization
* P1 Exposure Reconstruction
* P2 ETF Selection Audit
* P3-A Trend Persistence
* P3-B Drawdown Quality
* P3-C Trend Stability
* P3-D Weight Optimization
* MIG-007 Long-Term Robustness Validation
* P4-A Bull Market Filter
* P4-B Bull Risk Scaling
* P4-C1 Bull Allocation Audit

**Final Ranking Model:**

```python
Final Score = (
    0.50 * Momentum +
    0.15 * Trend Quality +
    0.15 * Trend Persistence +
    0.05 * Drawdown Quality +
    0.05 * Trend Stability +
    0.10 * Liquidity
)
```

---

## P4 Validation Results

### 2020 Bull Market

| Metric                                                |  Before |  After |
| ----------------------------------------------------- | ------: | -----: |
| Total Return                                          |  15.47% | 26.87% |
| Sharpe                                                |    0.93 |   1.03 |
| Sortino                                               |    1.21 |   1.37 |
| Max Drawdown                                          |   8.39% | 14.65% |
| Annual Excess Return                                  | -10.22% |  1.50% |
| Information Ratio                                     |   -0.81 |   0.14 |
| *Result: Bull-market capture improved significantly.* |         |        |

---

### 2022 Bear Market

| Metric                                                                          |  Before |   After |
| ------------------------------------------------------------------------------- | ------: | ------: |
| Total Return                                                                    | -12.02% | -10.73% |
| Max Drawdown                                                                    |  13.57% |  11.49% |
| Annual Excess Return                                                            |   9.21% |  10.55% |
| Information Ratio                                                               |    0.53 |    0.61 |
| *Result: Defensive characteristics improved without sacrificing excess return.* |         |         |

---

### 2024-2025 Mixed Market

| Metric                                                                       | Before |  After |
| ---------------------------------------------------------------------------- | -----: | -----: |
| Total Return                                                                 | 40.87% | 38.79% |
| Annual Return                                                                | 19.32% | 18.41% |
| Sharpe                                                                       |   1.40 |   0.91 |
| Max Drawdown                                                                 |  9.08% | 10.54% |
| Annual Excess Return                                                         |  2.45% |  1.40% |
| *Result: Performance deteriorated during the technology-led AI bull market.* |        |        |

---

## P4-C1 Bull Allocation Audit

### Objective

Identify which assets reduce long-term bull-market alpha before implementing allocation changes.

---

### P4-C1-001 Remove Gold (518880)

| Period    | Full ETF | Remove Gold |
| --------- | -------: | ----------: |
| 2020      |   26.87% |      34.95% |
| 2022      |  -10.73% |      -8.84% |
| 2024-2025 |   38.79% |      35.20% |

**Conclusion:**

`518880.SS` is not a confirmed alpha drag.

Gold behaves as a regime-dependent diversifier:

* Improves some bull markets
* Improves defensive performance
* Reduces performance in other regimes

**Decision:** Keep in the ETF universe.

---

### P4-C1-002 Remove HS300 (510300)

| Period    | Full ETF | Remove 510300 |
| --------- | -------: | ------------: |
| 2020      |   26.87% |        25.53% |
| 2022      |  -10.73% |       -10.73% |
| 2024-2025 |   38.79% |        45.67% |

**Conclusion:**

`510300.SS` is a confirmed bull-market alpha drag.

Evidence:

* No impact during bear markets
* Limited impact during 2020
* Significant improvement during 2024-2025
* Higher Sharpe, Sortino and Information Ratio
* Lower maximum drawdown

**Decision:**

Investigate reduced HS300 exposure during confirmed bull regimes.

---

### P4-C1-003 Remove CSI500 (510500)

| Period    | Full ETF | Remove 510500 |
| --------- | -------: | ------------: |
| 2020      |   26.87% |        32.36% |
| 2022      |  -10.73% |       -11.28% |
| 2024-2025 |   38.79% |        38.38% |

**Conclusion:**

`510500.SS` is a neutral broad-market diversifier.

No consistent alpha drag was observed.

**Decision:** Keep in the ETF universe.

---

### P4-C1-004 Technology-Only Portfolio

| Period    | Full ETF | Tech Only |
| --------- | -------: | --------: |
| 2020      |   26.87% |    -5.23% |
| 2022      |  -10.73% |    -8.81% |
| 2024-2025 |   38.79% |    31.78% |

**Conclusion:**

Technology concentration failed across all validation periods.

The strategy alpha comes from:

**Cross-sector rotation**

rather than:

**Pure technology exposure**

**Decision:**

Reject Tech Tilt as a future optimization path.

---

## Backtest Performance History

### Original Version

* Annual Return: 2.70%
* Sharpe: -0.17
* Max Drawdown: 5.28%

### P1 Exposure Reconstruction

* Annual Return: 13.72%
* Sharpe: 0.80
* Max Drawdown: 8.84%

### P2 Complete

* Annual Return: 15.58%
* Sharpe: 0.96
* Max Drawdown: 8.93%
* Alpha: 0.05
* Beta: 0.55
* Annual Excess Return: -1.03%

### P3 Final (2020-2026 Full Cycle)

| Metric               | Strategy |
| -------------------- | -------: |
| Total Return         |   62.71% |
| Annual Return        |    8.08% |
| Excess Return        |   43.73% |
| Annual Excess Return |    5.96% |
| Alpha                |     0.05 |
| Beta                 |     0.43 |
| Sharpe               |     0.37 |
| Sortino              |     0.50 |
| Max Drawdown         |   20.25% |
| Information Ratio    |     0.40 |

---

## Key Improvements

### P1

**Action:**

Removed excessive exposure suppression.

**Results:**

* Annual Return: 2.70% → 13.72%
* Sharpe: -0.17 → 0.80

---

### P2

**Action:**

ETF Universe Audit.

Removed:

`588000.SS`

**Results:**

* Annual Return: 13.72% → 15.58%
* Sharpe: 0.80 → 0.96
* Excess Return: -6.06% → -1.98%

---

### P4

**Action:**

Bull Market Enhancement.

**Results:**

* 2020 bull participation improved substantially
* 2022 defensive performance improved
* P4-C1 attribution analysis completed
* Future work will focus on large-cap de-emphasis rather than technology concentration

---

## Strategy Architecture

Universe → Data Layer → Indicator Layer → Ranking Engine → Bull Market Filter → Risk Budget Engine → Position Sizing → Execution Layer

---

## ETF Universe

### Broad Market ETFs

`510300`, `510500`, `512100`, `563300`, `159915`, `510880`

### Financial ETFs

`512880`, `512800`

### Technology ETFs

`512480`, `159819`, `562500`, `512980`, `516160`

### Defense ETFs

`512660`

### Healthcare ETFs

`512010`

### Consumer ETFs

`159928`

### Resource ETFs

`512400`, `518880`, `515220`

### Cash ETF

`511880`

---

## Ranking Factors

* **Momentum Score:** Measures trend strength and relative performance.
* **Quality Score:** Measures consistency and stability.
* **Trend Persistence:** Measures long-term trend continuity.
* **Drawdown Quality:** Penalizes unstable price behavior.
* **Trend Stability:** Rewards smoother trend development.
* **Liquidity Score:** Measures tradability.
* **Composite Score:** Final weighted ranking score.

---

## Risk Management

### ETF Trend Filter

**Requirement:**

```text
Close > MA200
```

---

### Bull Market Filter

**Current Rule:**

Bull regime is activated when at least two major broad-market ETFs remain above MA200.

**Purpose:**

Increase participation during sustained bull markets.

---

### Bull Risk Scaling

**Bull Market:**

```python
risk_factor = 1.0
```

**Non-Bull Market:**

```python
risk_factor = 0.5
```

---

### Risk Budget Engine

**Current Parameter:**

```python
TARGET_PORTFOLIO_RISK = 0.15
```

**Purpose:**

Control portfolio volatility while maintaining adequate market exposure.

---

### Cash ETF

Unused capital is allocated to:

```text
511880
```

---

## Execution Layer

**Execution Features:**

* Cash pre-check
* Commission buffer
* Sell-first execution
* Scaled buying
* Threshold protection

**Validation Status:**

Completed

---

## Major Design Decisions

### Decision 1: Remove Market Exposure Engine

**Reason:**

Duplicated ETF trend filtering and caused chronic underexposure.

**Validation:**

Backtest confirmed significant improvement in return and Sharpe ratio.

---

### Decision 2: Increase TARGET_PORTFOLIO_RISK

**Old:**

```python
0.10
```

**New:**

```python
0.15
```

**Reason:**

10% target risk was excessively conservative.

---

### Decision 3: Remove 588000.SS

**Reason:**

ETF Attribution Analysis identified persistent negative contribution.

**Validation:**

* Annual Return: 13.72% → 15.58%
* Sharpe: 0.80 → 0.96
* Drawdown unchanged

---

## Project Roadmap

### Completed

* P0 Execution Layer Stabilization
* P1 Portfolio Exposure Reconstruction
* P2 ETF Selection Audit
* P3 Ranking Engine Enhancement
* P4-A Bull Market Filter
* P4-B Bull Risk Scaling
* P4-C1 Bull Allocation Audit

---

### Current Phase:

P4-D Forward Stability Validation

Recent Improvements:

- Bull-market broad ETF preference
- Soft broad diversification penalties
- Better support for multi-theme bull markets
- Increased sector participation
- Improved full-cycle risk-adjusted returns

Latest Validation Results:

2020:

Return:

28.55%

Sharpe:

1.11

Max Drawdown:

14.87%

---

2024-2025:

Return:

41.74%

Sharpe:

0.97

Max Drawdown:

11.08%

---

2020-2026:

Return:

99.74%

Annualized:

11.67%

Sharpe:

0.43

Information Ratio:

0.63

Max Drawdown:

23.48%

---

### Future

* P5 Walk-Forward Validation
* P6 Production Deployment Review

---

## Important Notes

Before changing any parameter:

1. Run backtests.
2. Compare against baseline.
3. Update CHANGELOG.md.
4. Record performance metrics.

Rules:

* Do not modify multiple core modules simultaneously.
* Always validate changes incrementally.
* Every change must be supported by attribution analysis and backtest evidence.
