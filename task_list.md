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
IN PROGRESS

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
NOT STARTED

---

# Phase 9 - Validation

## TEST-001 Indicator Validation

Dependencies:

* IND-001
* IND-002
* IND-003
* IND-004
* IND-005
* IND-006

Status:
NOT STARTED

---

## TEST-002 Historical Backtest

Dependencies:
EXEC-002

Status:
NOT STARTED

---

## TEST-003 Paper Trading

Dependencies:
TEST-002

Status:
NOT STARTED

---

## TEST-004 Live Trading

Dependencies:
TEST-003

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