# ETF Rotation Strategy

## Overview

Multi-factor ETF rotation strategy for PTrade.

Core idea:

Select the strongest ETFs from a diversified ETF universe using:

* Multi-horizon risk-adjusted momentum
* Trend quality (slope × R²)
* Trend persistence
* Drawdown quality
* Liquidity filters
* ATR-based risk parity sizing
* Portfolio risk budgeting

The strategy is designed to:

* Participate in major market trends
* Avoid prolonged bear markets
* Rotate into stronger sectors
* Prefer smoother and more persistent trends
* Penalize high-drawdown assets
* Maintain controlled portfolio volatility


The strategy is designed to:

* Participate in major market trends
* Avoid prolonged bear markets
* Rotate into stronger sectors
* Maintain controlled portfolio volatility

---

## Current Status

## Current Status

Version:

P3 Final (Production Candidate)

Completed Modules:

* P0 Execution Layer Stabilization
* P1 Exposure Reconstruction
* P2 ETF Selection Audit
* P3-A Trend Persistence
* P3-B Drawdown Quality
* P3-C Trend Stability
* MIG-007 Long-Term Robustness Validation
* P3-D Weight Optimization

Final Ranking Model:

```python
Final Score =

0.50 * Momentum
+ 0.15 * Trend Quality
+ 0.15 * Trend Persistence
+ 0.05 * Drawdown Quality
+ 0.05 * Trend Stability
+ 0.10 * Liquidity
```

Full-Cycle Validation (2020-2026):

| Metric               | Strategy |
| -------------------- | -------- |
| Total Return         | 62.71%   |
| Annual Return        | 8.08%    |
| Excess Return        | 43.73%   |
| Annual Excess Return | 5.96%    |
| Alpha                | 0.05     |
| Beta                 | 0.43     |
| Sharpe               | 0.37     |
| Sortino              | 0.50     |
| Max Drawdown         | 20.25%   |
| Information Ratio    | 0.40     |

Status:

Production Candidate

Next Stage:

P4-A Bull Market Capture Enhancement

---

## Backtest Performance

### Original Version

Annual Return:
2.70%

Sharpe:
-0.17

Max Drawdown:
5.28%

---

### P1 Exposure Reconstruction

Annual Return:
13.72%

Sharpe:
0.80

Max Drawdown:
8.84%

---

### Current Version (P2 Complete)

Annual Return:
15.58%

Sharpe:
0.96

Max Drawdown:
8.93%

Alpha:
0.05

Beta:
0.55

Annual Excess Return:
-1.03%

---

## Key Improvements

### P1

Removed excessive exposure suppression.

Results:

* Annual Return:
  2.70% → 13.72%

* Sharpe:
  -0.17 → 0.80

---

### P2

ETF Universe Audit.

Removed:

* 588000.SS (STAR 50 ETF)

Results:

* Annual Return:
  13.72% → 15.58%

* Sharpe:
  0.80 → 0.96

* Excess Return:
  -6.06% → -1.98%

---

## Strategy Architecture

Universe

↓

Data Layer

↓

Indicator Layer

↓

Ranking Engine

↓

Risk Budget Engine

↓

Position Sizing

↓

Execution Layer

---

## ETF Universe

### Broad Market ETFs

* 510300
* 510500
* 512100
* 563300
* 159915
* 510880

### Financial ETFs

* 512880
* 512800

### Technology ETFs

* 512480
* 159819
* 562500
* 512980
* 516160

### Defense ETFs

* 512660

### Healthcare ETFs

* 512010

### Consumer ETFs

* 159928

### Resource ETFs

* 512400
* 518880
* 515220

### Cash ETF

* 511880

---

## Ranking Factors

### Momentum Score

Measures trend strength and relative performance.

### Quality Score

Measures consistency and stability.

### Liquidity Score

Measures tradability.

### Composite Score

Final weighted ranking score.

---

## Risk Management

### ETF Trend Filter

Requirement:

Close > MA200

---

### Risk Budget Engine

Current Parameter:

TARGET_PORTFOLIO_RISK = 0.15

Purpose:

Control portfolio volatility while maintaining adequate market exposure.

---

### Cash ETF

Unused capital is allocated to:

511880

---

## Execution Layer

### Execution Features

* Cash pre-check
* Commission buffer
* Sell-first execution
* Scaled buying
* Threshold protection

### Validation Status

Completed

---

## Major Design Decisions

### Decision 1

Remove Market Exposure Engine

Reason:

Duplicated ETF trend filtering and caused chronic underexposure.

Validation:

Backtest confirmed significant improvement in return and Sharpe ratio.

---

### Decision 2

Increase TARGET_PORTFOLIO_RISK

Old:

0.10

New:

0.15

Reason:

10% target risk was excessively conservative.

Validation:

Produced better risk-adjusted performance.

---

### Decision 3

Remove 588000.SS

Reason:

ETF Attribution Analysis and Removal Simulation identified persistent negative contribution.

Validation:

Annual Return:
13.72% → 15.58%

Sharpe:
0.80 → 0.96

Drawdown unchanged.

---

## Project Roadmap

### Completed

P0 Execution Layer Stabilization

P1 Portfolio Exposure Reconstruction

P2 ETF Selection Audit

---

### Current Phase

P3 Ranking Engine Enhancement

Goals:

* Audit ranking factors
* Improve ETF selection quality
* Analyze factor contribution
* Improve excess return generation

---

### Future

P4 Walk-Forward Validation

P5 Production Deployment Review

---

## Important Notes

Before changing any parameter:

1. Run backtests.

2. Compare against baseline.

3. Update CHANGELOG.md.

4. Record performance metrics.

Do not modify multiple core modules simultaneously.

Always validate changes incrementally.

Every change must be supported by attribution analysis and backtest evidence.
