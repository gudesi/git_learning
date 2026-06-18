# Task List

Project: Institutional China ETF Trend Following Portfolio v4.0

Status Legend:

* NOT STARTED
* IN PROGRESS
* DONE
* BLOCKED

---

# Phase 1 - Foundation Layer

## DATA-001 ETF Universe Definition

Description:
建立ETF池配置与分类体系。

Dependencies:
None

Deliverable

- CASH_ETF
- RISK_ETFS
- ETF_UNIVERSE
- ETF_CATEGORY_MAP
- ETF_NAME_MAP
- ASSET_CLASS_MAP
- validate_universe()

Definition of Done:

* ETF池包含20只风险ETF
* ETF池包含1只现金ETF
* 分类映射完成
* 单元测试通过

Status:
DONE

---

## DATA-002 Configuration Management

Description:
建立CONFIG统一参数管理体系。

Dependencies:
DATA-001

Deliverable:

* CONFIG

Definition of Done:

* 所有参数来自CONFIG
* 无硬编码参数
* 配置读取正常

Status:
DONE

---

## DATA-003 Data Access Layer

Description:
建立统一数据接口层。

Dependencies:
DATA-002

Deliverable:

* get_close()
* get_high()
* get_low()
* get_volume()
* get_turnover()

Definition of Done:

* 返回格式统一
* 支持全部ETF
* 数据长度正确
* 异常处理完成

Status:
DONE

---

## DATA-004 Portfolio Access Layer

Description:
建立Portfolio信息接口。

Purpose:
Provide unified access to
context.portfolio
and Position objects.

Dependencies:
DATA-003
STATE-001

Required By:
RISK-001
EXEC-001

Deliverable:

* get_equity()
* get_cash()
* get_positions()

Definition of Done:

* 返回值正确
* 实盘兼容
* 回测兼容

Status:
DONE

---

# Phase 2 - Indicator Layer

## IND-001 Return Calculation

Description:
计算多周期收益率。

Dependencies:
DATA-003

Deliverable:

* calc_return()

Definition of Done:

* 支持20日收益率
* 支持60日收益率
* 支持120日收益率
* 支持250日收益率

Status:
DONE

---

## IND-002 Volatility Calculation

Description:
计算60日年化波动率。

Dependencies:
DATA-003

Deliverable:

* calc_volatility()

Definition of Done:

* 年化处理正确
* NaN处理正确
* 单元测试通过

Status:
DONE

---

## IND-003 Momentum Score

Description:
计算Momentum Score。

Dependencies:

* IND-001
* IND-002

Deliverable:

* calc_momentum_score()

Definition of Done:

* 风险调整完成
* Percentile Rank完成
* 权重计算正确

Status:
DONE

---

## IND-004 Trend Quality

Description:
计算趋势质量评分。

Dependencies:
DATA-003

Deliverable:

* calc_quality_score()

Definition of Done:

* Log Price回归
* Slope计算正确
* R²计算正确
* 标准化完成

Status:
DONE

---

## IND-005 Liquidity Score

Description:
计算流动性评分。

Dependencies:
DATA-003

Deliverable:

* calc_liquidity_score()

Definition of Done:

* ADV60正确
* 标准化完成
* 排名正确

Status:
DONE

---

## IND-006 ATR

Description:
计算ATR20。

Dependencies:
DATA-003

Deliverable:

* calc_atr()

Definition of Done:

* ATR20正确
* 边界情况处理
* 单元测试通过

Status:
DONE

---

FIX-001 Development Infrastructure Cleanup

Definition of Done:

see Development Notes at the bottom

Status:
DONE

# Phase 3 - Market Filter

## FILTER-001 Market Breadth

Description:
计算市场评分。

Dependencies:
DATA-003

Deliverable:

* calc_market_score()

Definition of Done:

* 沪深300评分正确
* 中证500评分正确
* 中证1000评分正确

Status:
DONE

---

## FILTER-002 Market Exposure

Description:
根据市场评分计算目标仓位。

Dependencies:
FILTER-001

Deliverable:

* calc_market_exposure()

Definition of Done:

* 0分=0%
* 1分=50%
* 2分=80%
* 3分=100%

Status:
DONE

---

# Phase 4 - Ranking Layer

## RANK-001 Final Score

Description:
计算Final Score。

Dependencies:

* IND-003
* IND-004
* IND-005

Deliverable:

* calc_final_score()

Definition of Done:

* 权重正确
* 排名正确
* 排序稳定

Status:
DONE

---

## RANK-002 ETF Selection

Description:
生成目标持仓池。

Dependencies:

* FILTER-001
* RANK-001

Deliverable:

* select_etfs()

Definition of Done:

* Top5选取正确
* MA200过滤正确
* 递补机制正确

Status:
DONE

Notes:
- Architecture review completed after implementation.
- Fixed BUG-004 (account interface context handling).
- Fixed BUG-005 (cash interface context handling).
- Added validate_ranking_pipeline().
- Full ranking pipeline validation currently requires PTrade runtime.
- Ranking cache optimization deferred until PORT layer.
---

# Phase 5 - Portfolio Layer

## PORT-001 Position Sizing

Description:
风险平价权重计算。

Dependencies:

* IND-006
* RANK-002

Deliverable:

* calc_weights()

Definition of Done:

* ATR权重正确
* 权重归一化正确

Status:
DONE

---

## PORT-002 Portfolio Constraints

Description:
组合约束管理。

Dependencies:
PORT-001

Deliverable:

* apply_constraints()

Definition of Done:

* 单ETF≤25%
* 单类≤40%
* 权重归一化

Status:
DONE

notes:

Implemented:
- Weight normalization
- Maximum position constraint
- Minimum position constraint
- Constraint validation

Post-implementation fixes:
- Replaced single-pass max position constraint with iterative water-filling algorithm.
- Added unified constraint convergence loop.
- Added validation tests for overweight and minimum-position edge cases.

---

# Phase 6 - Risk Layer

## RISK-001 ATR Stop

Description:
ATR止损管理。

Dependencies:

* IND-006
* STATE-001

Deliverable:

* update_stop_price()

Definition of Done:

* 止损位正确
* 更新正确

Status:
DONE

---

## RISK-002 Exit Rules

Description:
退出信号管理。

Dependencies:

* RISK-001
* FILTER-001

Deliverable:

* generate_exit_signals()

Definition of Done:

* MA200退出
* ATR退出
* 市场退出

Status:
DONE

---

# Phase 7 - State Management

## STATE-001 Strategy State

Description:
建立状态管理系统。

Dependencies:
DATA-002

Deliverable:

* strategy_state

Definition of Done:

* entry_price
* entry_date
* stop_price
* highest_close

全部正常维护

Status:
DONE

---

# Phase 8 - Execution Layer

## EXEC-001 Order Mapping

Description:
建立PTrade交易映射层。

Dependencies:
DATA-004

Deliverable:

* order_target_value()
* order_target_percent()

Definition of Done:

* 回测兼容
* 实盘兼容

Status:
DONE

---

## EXEC-002 Rebalance Engine

Description:
实现统一调仓引擎。

Dependencies:

* EXEC-001
* PORT-002

Deliverable:

* rebalance()

Definition of Done:

* 买卖逻辑正确
* 现金检查正确
* 调仓正确

Status:
DONE

---

# Phase 9 - PTrade Migration

## MIG-001A

PTrade Lifecycle

新增：

initialize()

before_trading_start()

after_trading_end()

完成标准：

策略成功加载

Status:
DONE

Verified:
- initialize(context)
- before_trading_start(context, data)
- after_trading_end(context, data)

Successfully executed in PTrade.

## MIG-001B Environment Validation

Description:
Validate PTrade runtime environment and
portfolio object structure.

Verification Results:

✓ context object accessible

✓ context.portfolio accessible

✓ context.portfolio.cash verified

✓ context.portfolio.total_value verified

✓ context.portfolio.positions verified

Key Findings:

cash:
context.portfolio.cash

total_value:
context.portfolio.total_value

positions:
context.portfolio.positions

Status:
DONE

## MIG-001C Scheduler Validation

Description:
Validate PTrade scheduled task execution.

Verification Results:

✓ run_daily() registration successful

✓ scheduled callback executed

✓ callback executed once per trading day

✓ callback executed at configured time

Test Function:

daily_heartbeat()

Observed Schedule:

14:50 each trading day

Status:
DONE

## MIG-002 Data Interface Migration
目标：

彻底替换Stub。

检查：

_get_history_field()

get_price()

get_volume()

get_high()

get_low()

get_close()

全部改成：

get_history()

真实PTrade接口。

完成标准：

下面代码运行成功：

calculate_atr()

calculate_momentum()

calculate_quality()

全部返回真实数据。

Status:
DONE

## MIG-003 Portfolio Interface Validation
目标：

验证：

context.portfolio

与当前封装一致。

检查：

get_positions()

get_position()

get_cash()

get_total_value()

完成标准：

打印：

context.portfolio

验证：

cash

positions

total_value

字段全部存在。

Status:
DONE

## MIG-004 Execution Interface Migration
目标：

替换：

order_target_percent()

order_target_value()

封装。

验证：

buy_cash_etf()

rebalance_portfolio()

实际能够下单。

完成标准：

模拟盘产生真实订单。

Status:
DONE

## MIG-005 = Core Strategy Integration

Goal:
Integrate the validated strategy engine into the PTrade runtime environment.

Prerequisites:
- MIG-001 Lifecycle Review Passed
- MIG-002 Data Interface Review Passed
- MIG-003 Portfolio Mapping Review Passed
- MIG-004 Order Mapping Review Passed
- Migration Layer v1.0 Frozen

Tasks:

[MIG-005A] Indicator Integration
Status: Completed

Completed:
- RETURN_WINDOWS migrated
- ATR_LOOKBACK migrated
- LIQUIDITY_LOOKBACK migrated
- QUALITY_LOOKBACK migrated
- MOMENTUM_WEIGHTS migrated

- IND-001 Return Calculation
- IND-002 Volatility Calculation
- IND-003 Momentum Score
- IND-004 Trend Quality Score
- IND-005 Liquidity Score
- IND-006 ATR20

- get_turnover() migrated
- turnover -> money field mapping validated

Validation:
- _get_history_field() DataFrame compatibility verified
- ETF symbol suffix mapping validated (.SS / .SZ)
- Cross-sectional ranking validated
- Momentum score validated
- Quality score validated

MIG-005B Filter Integration
Status: DONE

Integrate:
- FILTER-001 Market Breadth
- FILTER-002 Market Exposure

Dependencies:
- MIG-005A


MIG-005C Ranking Integration
Status: DONE

Integrate:
- RANK-001 Final Score
- RANK-002 ETF Selection

Dependencies:
- MIG-005A
- MIG-005B


MIG-005D Portfolio Integration
Status: DONE

Integrate:
- PORT-001 Position Sizing
- PORT-002 Portfolio Constraints

Dependencies:
- MIG-005C


MIG-005E Risk Integration
Status: DONE

Integrate:
- RISK-001 Portfolio Risk Engine
- RISK-002 Portfolio Risk Control

Dependencies:
- MIG-005D


MIG-005F Execution Integration
Status: DONE

Integrate:
- EXEC-001 Order Mapping Layer
- EXEC-002 Rebalance Engine

Dependencies:
- MIG-005E


MIG-005G Scheduler Integration
Status: DONE

Integrate:
- strategy_main()
- run_daily()
- rebalance()

Dependencies:
- MIG-005F


# Post-Migration Performance Optimization


Status: In Progress

Background:
After MIG-005A ~ MIG-005G completion, full strategy integration is functional.
Post-migration review identified significant performance degradation:

- Backtest runtime increased from ~1 minute to 10-30 minutes
- Indicator calculations repeatedly request historical data
- Ranking pipeline executes multiple times per rebalance
- Portfolio weight calculations are recomputed unnecessarily
- Original caching layer was not migrated

Objective:
Restore near pre-migration performance while preserving all migrated functionality.


## PERF-001 Cache Infrastructure
Status: DONE


Implement global cache layer:

- GLOBAL_CACHE dictionary
- clear_cache()
- cache_get()
- cache_set()

Requirements:

- Cache lifetime = one strategy cycle
- Cache cleared at strategy_main() start
- No modifications to context object
- All future performance optimizations use GLOBAL_CACHE

Dependencies:
None


## PERF-002 History Data Cache
Status: DONE

Add cache support to expensive indicator calculations:

Functions:

- _get_history_field()

Goals:

- Avoid repeated _get_history_field() calls
- Reuse results within same strategy cycle

Dependencies:
PERF-001


## PERF-003 Ranking Cache
Status: DONE


Add cache support to ranking pipeline:

Functions:

- calc_final_score()

Goals:

- Each ETF score calculated once per cycle
- Reuse ranking results across portfolio construction

Dependencies:
PERF-002

## REVIEW-008
Execution Order Sequencing Review

Status:
Deferred

Findings:
Order submission sequence may affect capital allocation efficiency.

Impact:
Low

Priority:
Low

Resolution:
Future EXEC optimization phase.


## PERF-004 Portfolio Cache
Status: DONE

Add cache support to portfolio construction:

Functions:

- get_selected_etfs()
- calc_target_weights()
- calc_risk_adjusted_weights()
- calc_market_exposure()

Goals:

- Eliminate duplicate ranking execution
- Eliminate duplicate target weight calculation
- Eliminate duplicate risk-adjusted weight calculation

Dependencies:
PERF-003

Implemented:
- target_weights cache
- ranking_table cache reuse
- portfolio construction cache flow

Verified:
- Multi-day backtest passed
- No duplicate ranking execution observed


## PERF-005 Performance Validation
Status: Pending


Validation:

- Compare runtime before/after optimization
- Verify identical portfolio outputs
- Verify no cache contamination between cycles
- Verify rebalance execution unchanged

Success Criteria:

- Significant runtime reduction
- No functional changes
- All MIG-005 functionality preserved

Dependencies:
PERF-004


## MIG-006 Backtest Validation
目标：

PTrade回测。

先跑：

2024-01-01
~
2025-12-31

检查：

调仓次数

持仓变化

现金ETF

是否正确。

完成标准：

回测完整结束。

无异常。

Status:
NOT STARTED

## MIG-007 Simulation Validation
目标：

PTrade模拟盘。

运行：

2~4周

检查：

订单提交

订单成交

仓位同步

日志输出

完成标准：

所有交易逻辑正常。

Status:
NOT STARTED

## MIG-008 Production Readiness Review
最终Code Review。

重点检查：

DATA
FILTER
RANK
PORT
RISK
EXEC
MIG

全链路。

确认：

无Stub

无TODO

无Mock

无临时Patch

完成标准：

允许实盘。

Status:
NOT STARTED

---

# Bug Backlog

| ID      | Description | Priority | Status |
| ------- | ----------- | -------- | ------ |
| BUG-001 | Reserved    | -        | Open   |
| BUG-002 | Reserved    | -        | Open   |
| BUG-003 | Reserved    | -        | Open   |

## Development Notes

### FIX-001 Infrastructure Cleanup

Completed before FILTER-001:

- Added PTrade API stubs
- Added logging interfaces
- Normalized DATA-004 account API naming
- Removed VSCode static analysis errors

This change does not introduce new strategy functionality and is not tracked as a standalone milestone.

[Done] FILTER-002 / RISK-002 Integration
- Market exposure now participates in final portfolio sizing.
- Final portfolio allocation:
  Target Weight × Market Exposure × Risk Scaling.

[Done] EXEC-002 Cash ETF Execution
- Residual cash allocation is automatically deployed into CASH_ETF.
- Cash ETF included in rebalance target universe.
- Prevents unnecessary sell/rebuy cycles during rebalancing.