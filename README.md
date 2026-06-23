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

P1 Exposure Reconstruction Complete

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

---

## Backtest Performance

Original Version

Annual Return:
2.70%

Sharpe:
-0.17

Max Drawdown:
5.28%

---

Current Version

Annual Return:
13.65%

Sharpe:
0.79

Max Drawdown:
8.82%

---

Key Improvement:

Removed excessive exposure suppression.

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

Broad Market ETFs

* 510300
* 510500
* 512100
* 563300

Sector ETFs

* 512400
* 512800
* 512480
* 512660
* 512880
* 512980
* 515220
* 516160
* 588000
* 159819
* 159915

Defensive Assets

* 518880
* 511880

---

## Ranking Factors

Momentum Score

Measures trend strength and relative performance.

Quality Score

Measures consistency and stability.

Liquidity Score

Measures tradability.

Composite Score

Final weighted ranking score.

---

## Risk Management

ETF Trend Filter

Requirement:

Close > MA200

---

Risk Budget Engine

Current Parameter:

TARGET_PORTFOLIO_RISK = 0.15

Purpose:

Reduce exposure during high-volatility periods.

---

Cash ETF

Unused capital is allocated to:

511880

---

## Execution Layer

Execution Features

* Cash pre-check
* Commission buffer
* Sell-first execution
* Scaled buying
* Threshold protection

Validation Status

Completed

---

## Major Design Decisions

Decision 1

Remove Market Exposure Engine

Reason:

Duplicated ETF trend filtering and caused chronic underexposure.

Backtest validation confirmed significant performance improvement.

---

Decision 2

Increase TARGET_PORTFOLIO_RISK

Old:

0.10

New:

0.15

Reason:

10% target risk was excessively conservative.

15% produced the best risk-adjusted performance.

---

## Project Roadmap

Completed

P0 Execution Layer Stabilization

P1 Portfolio Exposure Reconstruction

---

Next

P2 ETF Selection Audit

Goals:

* Identify negative expectancy ETFs
* Reduce asset universe
* Improve portfolio quality

---

Future

P3 Ranking Engine Enhancement

P4 Walk-Forward Validation

---

## Important Notes

Before changing any parameter:

1. Run backtests.

2. Compare against baseline.

3. Update CHANGELOG.md.

4. Record performance metrics.

Do not modify multiple core modules simultaneously.

Always validate changes incrementally.
