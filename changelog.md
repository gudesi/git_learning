
# 2026-06-28

## P4-C2 Soft Broad Diversification Penalty

Date:

2026-06

Changes:

Replaced hard broad-category exclusion
with a soft diversification penalty.

Old Logic:

Reject broad ETFs once the limit was reached.

New Logic:

broad_count=0:

1.00

broad_count=1:

0.95

broad_count=2:

0.90

broad_count>=3:

0.85

Results:

2020:

26.87% -> 28.55%

2024-2025:

38.79% -> 41.74%

2020-2026:

62.71% -> 99.74%

Annualized:

8.08% -> 11.67%

Information Ratio:

0.40 -> 0.63

Trade-off:

Maximum Drawdown:

20.25% -> 23.48%

Decision:

Accepted.

Reason:

The improvement was consistent across
multiple market regimes and outweighed
the moderate increase in drawdown.

## P4-C1 Bull Allocation Audit (Completed)

Objective:

Determine whether specific ETFs dilute returns during bull markets
before implementing P4-C2 Bull Allocation Tilt.

---

### P4-C1-001 Remove Gold (518880)

Results:

2020:
26.87% → 34.95%

2022:
-10.73% → -8.84%

2024-2025:
38.79% → 35.20%

Conclusion:

518880 is NOT a confirmed alpha drag.

Gold behaves as a regime-dependent diversifier:

- Dilutes some equity bull markets
- Improves other market environments
- Provides drawdown diversification

Decision:

Keep 518880 in the ETF universe.

---

### P4-C1-002 Remove HS300 (510300)

Results:

2020:
26.87% → 25.53%

2022:
-10.73% → -10.73%

2024-2025:
38.79% → 45.67%

Conclusion:

510300 is a confirmed bull-market alpha drag.

Evidence:

- Minimal impact on 2020
- No impact on 2022
- Significant improvement during 2024-2025
- Higher Sharpe, Sortino and Information Ratio
- Lower maximum drawdown

Decision:

Mark 510300 as a candidate for reduced exposure
during confirmed bull regimes.

---

### P4-C1-003 Remove CSI500 (510500)

Results:

2020:
26.87% → 32.36%

2022:
-10.73% → -11.28%

2024-2025:
38.79% → 38.38%

Conclusion:

510500 is not a confirmed alpha drag.

It acts as a neutral broad-market diversifier:

- Helps some market environments
- Hurts others
- No material impact during 2024-2025

Decision:

Keep 510500 in the ETF universe.

---

### P4-C1-004 Tech Only Portfolio

Configuration:

RISK_ETFS = TECH_ETFS

Results:

2020:
26.87% → -5.23%

2022:
-10.73% → -8.81%

2024-2025:
38.79% → 31.78%

Conclusion:

Technology concentration does not improve robustness.

The strategy alpha comes from:

Cross-sector rotation

rather than

pure technology exposure.

Decision:

Reject Tech Tilt as a future optimization direction.

---

P4-C1 Status:

COMPLETED

Key Findings:

518880:
Regime-dependent diversifier.

510500:
Neutral diversifier.

510300:
Confirmed bull-market alpha drag.

Tech-only portfolios:
Failed across all validation periods.

Next Stage:

P4-C2 Bull Large-Cap De-emphasis

# 2026-06-27

## P4-C1 Bull Allocation Audit (In Progress)

### Bull Market Filter Validation

Backtests completed:

2020:

15.47% → 26.87%

Sharpe:

0.93 → 1.03

2022:

-12.02% → -10.73%

Max drawdown:

13.57% → 11.49%

2024-2025:

40.87% → 38.79%

Sharpe:

1.40 → 0.91

Findings:

Bull regime improvements significantly enhanced
2020 and 2022 robustness,
but reduced performance during the 2024-2025 AI-driven market.

Preliminary observations:

* Technology ETF (159819) exposure decreased.
* Broad-market ETFs (510300, 510500) received larger allocations.
* Gold ETF (518880) remained in bull allocations.

P4-C1 remains open pending
detailed allocation attribution analysis.


# 2026-06-26

## MIG-007 Long-Term Robustness Validation

Status:
Completed

### Test Results

| Period    | Market Regime             | Result       |
| --------- | ------------------------- | ------------ |
| 2020      | COVID Crash + Bull Market | PARTIAL PASS |
| 2021      | Sector Rotation           | PASS         |
| 2022      | Bear Market               | PASS+        |
| 2023      | Sideways Market           | PASS+        |
| 2020-2026 | Full Cycle                | PASS         |

### Full Cycle Performance (2020-2026)

| Metric               | Result |
| -------------------- | ------ |
| Total Return         | 62.71% |
| Annual Return        | 8.08%  |
| Benchmark Return     | 20.66% |
| Excess Return        | 43.73% |
| Annual Excess Return | 5.96%  |
| Alpha                | 0.05   |
| Beta                 | 0.43   |
| Sharpe               | 0.37   |
| Sortino              | 0.50   |
| Max Drawdown         | 20.25% |
| Information Ratio    | 0.40   |

### Conclusion

No obvious overfitting was detected.

The P3 ranking enhancements remained effective across:

* Bull markets
* Bear markets
* Sideways markets
* Extreme market events

Decision:

PASS

---

## P3-D Weight Optimization

Date:
2026-06-26

Status:
Completed

### Candidate Weights

| Version | Weights          | Result   |
| ------- | ---------------- | -------- |
| A       | 50/15/15/5/5/10  | KEEP     |
| B       | 45/15/15/10/5/10 | ROLLBACK |
| C       | 45/15/15/5/10/10 | ROLLBACK |
| D       | 45/15/15/5/5/15  | OPTIONAL |
| E       | 55/10/10/5/5/15  | ROLLBACK |

### Final Production Weights

```python
Momentum      50%
Quality       15%
Persistence   15%
Drawdown       5%
Stability      5%
Liquidity     10%
```

### Conclusion

The original P3-C weights remained the strongest configuration across the full 2020-2026 validation period.

Decision:

NO CHANGE


# 2026-06-25

## P3-A Trend Persistence Factor

Status:
Completed

### Changes

Added a new Trend Persistence factor to improve ranking stability.

Implementation:

* Added `calc_trend_persistence_raw()`
* Measured the percentage of days above MA20 over the last 120 trading days
* Added cross-sectional percentile ranking
* Updated final ranking weights:

```python
Momentum      60%
Quality       15%
Persistence   15%
Liquidity     10%
```

### Backtest Results

Compared with P2 baseline:

| Metric            | P2     | P3-A   |
| ----------------- | ------ | ------ |
| Total Return      | 32.27% | 32.27% |
| Annual Return     | 15.58% | 15.57% |
| Sharpe            | 0.96   | 0.97   |
| Max Drawdown      | 8.93%  | 7.78%  |
| Excess Return     | -1.98% | -1.63% |
| Information Ratio | -0.09  | -0.07  |
| Win Rate          | 53.67% | 55.24% |
| Profit Factor     | 204.39 | 229.84 |
| Avg Holding Days  | 21.05  | 22.84  |

### Conclusion

Trend Persistence improved portfolio quality and reduced drawdowns without sacrificing returns.

Decision:

## KEEP

## P3-B Drawdown Quality Factor

Date:
2026-06-25

Status:
Completed

### Changes

Added a Drawdown Quality factor to penalize high-drawdown ETFs.

Implementation:

* Added `calc_max_drawdown_raw()`
* Used:

```python
drawdown_score = 1.0 - max_drawdown
```

* Added cross-sectional percentile ranking
* Updated final ranking weights:

```python
Momentum      55%
Quality       15%
Persistence   15%
Drawdown       5%
Liquidity     10%
```

### Backtest Results

Compared with P2 baseline:

| Metric               | P2     | P3-B   |
| -------------------- | ------ | ------ |
| Total Return         | 32.27% | 35.87% |
| Annual Return        | 15.58% | 17.19% |
| Excess Return        | -1.98% | 1.97%  |
| Annual Excess Return | -1.03% | 1.01%  |
| Alpha                | 0.05   | 0.06   |
| Beta                 | 0.55   | 0.54   |
| Sharpe               | 0.96   | 1.11   |
| Sortino              | 1.38   | 1.59   |
| Max Drawdown         | 8.93%  | 7.68%  |
| Information Ratio    | -0.09  | 0.08   |
| Win Rate             | 53.67% | 56.62% |
| Profit Factor        | 204.39 | 245.94 |
| Avg Holding Days     | 21.05  | 23.88  |

### Conclusion

The Drawdown Quality factor significantly improved risk-adjusted returns and turned excess returns positive while maintaining a low beta profile.

Decision:

KEEP

P3-A + P3-B are now part of the production ranking engine.


## 2026-06-24

## P2 ETF Selection Audit Completed

Analysis:

Performed ETF-level attribution analysis using:

* Trade history
* Position history
* Removal simulations

Universe Changes:

Removed:

* 588000.SS (STAR 50 ETF)

Rationale:

Attribution Analysis:

* Negative contribution
* Low win rate
* Poor profit/loss ratio

Removal Simulation:

* Annualized return improved:
  13.72% -> 15.58%

* Sharpe improved:
  0.80 -> 0.96

* Excess return improved:
  -6.06% -> -1.98%

* Maximum drawdown unchanged

Retained After Review:

* 512660.SS
* 512800.SS

Final Decision:

Remove 588000.SS from ETF universe.


# 2026-06-22

## Version: P1 Exposure Reconstruction Complete

### Added

* Exposure audit framework
* Risk budget audit metrics
* Market exposure audit metrics
* Portfolio exposure summary reporting

### Changed

* Removed Market Exposure Engine
* calc_market_exposure() now returns 1.0
* TARGET_PORTFOLIO_RISK increased from 0.10 to 0.15

### Validated

Backtest Period:

2024-06-01 ~ 2026-06-01

Performance:

Annual Return:
2.70% -> 13.65%

Sharpe:
-0.17 -> 0.79

Max Drawdown:
5.28% -> 8.82%

### Conclusion

P1 completed successfully.

Root cause of chronic underperformance was excessive exposure suppression caused by:

* Market Exposure Engine
* Overly conservative Risk Budget target

Exposure bottleneck resolved.

Next phase:

P2 ETF Selection Audit.


# 2026-06-22

## P0 Execution Layer officially completed.

Completed:

- EXEC-001 Cash Check
- EXEC-002 Commission Buffer
- EXEC-003 Sell First
- EXEC-004 Scaled Buy
- EXEC-005 Threshold Bug Fix

Validated through long-term backtest:

2024-06-01 ~ 2026-06-01

No execution-layer failures observed.

--------------------------------------------------

Added Exposure Audit framework.

New metrics:

- AVG_CASH_WEIGHT
- CASH_GT_50_PCT
- CASH_GT_80_PCT
- AVG_RISK_FACTOR
- AVG_MARKET_FACTOR
- AVG_FINAL_FACTOR

Audit findings:

- Average cash allocation >80%
- Risk exposure typically 10%-20%
- Market exposure heavily constrained
- Risk factor remained near defensive level

Conclusion:

Low performance is no longer believed to be caused by execution issues.

Focus shifted from execution layer to exposure layer.

Next phase:

P1-B Risk Budget Engine Audit

[EXEC-005] Threshold Bug Fix

- Fixed threshold scope bug in order_target_percent()
- Threshold filtering now applies only to buy orders
- Sell orders and REMOVE liquidation bypass threshold checks
- Validated with REMOVE scenarios on 2024-07-22 and 2024-07-24
- Passed full PTrade backtest (2024-06-01 ~ 2026-06-01)

[EXEC-001]
Added minimum order threshold.

- Introduced MIN_ORDER_VALUE = 12000
- Reduced zero-share ETF orders
- Reduced order spam warnings

Status:
Partially successful

Known Issue:
threshold variable causes
UnboundLocalError during sell orders.

Requires fix before MIG-006 completion.

# 2026-06-21

## MIG-006 Completed

完成PTrade长周期回测验证。

回测区间：

2024-01-01
~
2026-06-01

验证内容：

- 调仓流程
- 持仓识别
- 订单执行
- 现金ETF逻辑
- 长周期稳定性

结果：

PASS

---

## EXEC-001 Cash Management Fix

问题：

订单执行阶段偶发资金不足。

修复：

- 引入 COMMISSION_BUFFER
- 调整目标仓位计算

结果：

- 不再出现资金不足
- 不再出现现金不足
- 长周期回测稳定

---

## EXEC-002 Diagnostics Logging

新增：

- CURRENT 持仓日志
- TARGET 目标持仓日志
- REMOVE 卖出集合日志
- BUY / SELL 调仓日志

结果：

执行层行为可追踪。

---

## Project Milestone
项目进入：

 P0 - 先修执行层

已确认成功将代码迁移至ptrade，回测无语法错误，性能良好。将之前的代码删除，目标从编写代码改为优化策略，提高盈利能力。