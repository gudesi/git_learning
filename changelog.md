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