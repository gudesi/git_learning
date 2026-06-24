# ETF Rotation Strategy

## Overview

Multi-factor ETF rotation strategy for PTrade.

Core idea:

Select the strongest ETFs from a diversified ETF universe using trend, momentum, quality, liquidity and risk controls.

The strategy is designed to:

* Participate in major market trends
* Avoid prolonged bear markets
* Rotate into stronger sectors
* Maintain controlled portfolio volatility

---

## Current Status

Version:

P2 ETF Selection Audit Complete

Backtest Period:

2024-06-01 ~ 2026-06-01

Current Best Configuration:

Market Exposure Engine:
Removed

Target Portfolio Risk:
15%

ETF Trend Filter:
MA200

Position Count:
5

ETF Universe:
588000.SS Removed

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
