# P0 - Execution Layer Stabilization

Status: Completed

EXEC-001 Cash Check
Status: Completed

EXEC-002 Commission Buffer
Status: Completed

EXEC-003 Sell First
Status: Completed

EXEC-004 Scaled Buy
Status: Completed

EXEC-005 Threshold Bug Fix
Status: Completed

Validation:

✓ Long-term backtest passed
(2024-06-01 ~ 2026-06-01)

✓ REMOVE successfully liquidates positions

✓ No ORDER_TARGET_PERCENT_EXCEPTION

✓ No UnboundLocalError

✓ Positions update correctly

---

# P1 - Portfolio Exposure Reconstruction

Status: Completed

Goal:

Identify root cause of chronic underperformance.

Original Backtest
(2024-06-01 ~ 2026-06-01)

Return:
5.29%

---

## P1-A Exposure Audit

Status: Completed

Audit Summary:

AUDIT_DAYS=400

AVG_CASH_WEIGHT=0.8000

CASH_GT_50_PCT=71.25%

CASH_GT_80_PCT=52.25%

AVG_RISK_FACTOR=0.5019

AVG_MARKET_FACTOR=0.3962

AVG_FINAL_FACTOR=0.2000

Conclusion:

Strategy remained in a highly defensive state.

Average risk exposure was only 20%.

Cash allocation averaged 80%.

---

## P1-B Risk Budget Engine Audit

Status: Completed

Findings:

1. Portfolio volatility uses weighted-average volatility rather than true covariance-based portfolio volatility.

2. TARGET_PORTFOLIO_RISK=10% was likely too conservative.

3. Risk Budget Engine reduced exposure materially.

4. Market Exposure Engine remained the dominant source of underexposure.

---

## P1-C Market Exposure Review

Status: Completed

Findings:

1. AVG_MARKET_FACTOR=0.3962

2. Market Exposure Engine was the primary source of chronic underexposure.

3. MA50 > MA100 > MA200 trend definition was excessively strict.

4. Trend filtering existed at both market level and ETF level.

---

## P1-D Market Filter Redesign

Status: Completed

Backtest Validation:

Replace:

def calc_market_exposure()

with:

return 1.0

Result:

Annual Return:
2.70% -> 10.13%

Sharpe:
-0.17 -> 0.55

Max Drawdown:
5.28% -> 8.79%

Conclusion:

Market Exposure Engine duplicated ETF trend filtering and significantly reduced performance.

Decision:

Remove Market Exposure Engine.

Final Implementation:

def calc_market_exposure():
return 1.0

---

## P1-E Risk Budget Engine Review

Status: Completed

Sensitivity Test:

Target Risk = 10%

Annual Return:
10.13%

Sharpe:
0.55

Max DD:
8.79%

---

Target Risk = 15%

Annual Return:
13.65%

Sharpe:
0.79

Max DD:
8.82%

---

Target Risk = 20%

Annual Return:
13.61%

Sharpe:
0.70

Max DD:
9.75%

Conclusion:

TARGET_PORTFOLIO_RISK=10%
is too conservative.

TARGET_PORTFOLIO_RISK=15%
provides the best risk-adjusted performance.

Increasing target risk beyond 15%
does not improve returns and increases drawdown.

Decision:

TARGET_PORTFOLIO_RISK = 0.15

---

P1 Final Result

Original Strategy:

Annual Return:
2.70%

Sharpe:
-0.17

Max DD:
5.28%

---

After P1 Reconstruction:

Annual Return:
13.65%

Sharpe:
0.79

Max DD:
8.82%

Conclusion:

The primary cause of underperformance was excessive exposure suppression.

P1 successfully resolved the exposure bottleneck.

---

# P2 - ETF Selection Audit

Status: Ready

Goal:

Identify ETFs that consistently destroy alpha.

Focus:

1. Per-ETF contribution analysis

2. Win/loss distribution analysis

3. Negative expectancy ETF identification

4. Out-of-sample validation before removal

Candidate ETFs requiring review:

588000.XSHG

512660.XSHG

159915.XSHE

515220.XSHG

Expected Outcome:

Reduce asset universe.

Improve signal quality.

Improve portfolio expectancy.

---

# P3 - Ranking Engine Enhancement

Status: Pending

Goal:

Improve ranking quality.

Potential Work:

* Reduce Quality Score weight

* Reduce Liquidity Score weight

* Add trend persistence

* Add drawdown penalty

* Add slope stability factor

* Recalibrate ranking weights

---

# P4 - Walk-Forward Validation

Status: Pending

Goal:

Perform rolling out-of-sample validation.

Tasks:

* Rolling optimization

* Walk-forward testing

* Parameter stability analysis

* Robustness verification

Success Criteria:

Strategy remains profitable across unseen periods without parameter re-tuning.
