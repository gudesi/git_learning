# Changelog

All notable changes to this project will be documented in this file.

Format:

* Added
* Changed
* Removed
* Fixed

## 2026-06-14

## [Migration] MIG-004 Order Interface Validation Completed

### Added

- Implemented MIG-004 order interface validation suite
- Verified order_target_value() execution behavior
- Verified order ID return type (str)
- Verified zero-share order behavior (returns None)
- Verified automatic buy/sell adjustment toward target value
- Verified get_open_orders() API availability

### Documented

- Added PTrade Order Mapping reference
- Recorded order submission and return-value semantics
- Recorded target-position execution behavior

### Result

MIG-004 validation passed.
Core order-management APIs confirmed compatible with strategy migration requirements.

### MIG-003 Portfolio Interface Validation Completed

Validated PTrade portfolio interfaces using live backtest execution.

Verified:

- context.portfolio access
- portfolio.cash
- portfolio.total_value
- portfolio.positions
- portfolio.positions_value
- portfolio.returns
- Position object attributes
- order_target_value() execution
- position iteration workflow

Confirmed Position fields:

- sid
- amount
- enable_amount
- cost_basis
- last_sale_price
- today_amount

Validated portfolio state updates and order execution behavior during backtest.

## 2026-06-13

## [MIG-002] Data Interface Migration Completed

### Added

* Migrated DATA-003 historical market data interface into PTrade runtime.
* Added `_get_history_field()` PTrade adapter implementation.
* Added `get_close()` wrapper.
* Added `get_high()` wrapper.
* Added `get_low()` wrapper.
* Added `get_volume()` wrapper.
* Added `validate_data_interface()` migration validation routine.

### Validated

* PTrade `get_history()` API successfully invoked.
* Historical close price retrieval validated.
* Historical high price retrieval validated.
* Historical low price retrieval validated.
* Historical volume retrieval validated.
* Rolling lookback window behavior validated.
* 252-day historical data retrieval validated.

### PTrade Compatibility Notes

* Shanghai market securities require `.SS` suffix.
* Shenzhen market securities require `.SZ` suffix.
* PTrade `get_history()` returns pandas DataFrame objects.
* Historical data interface confirmed compatible with downstream indicator layer requirements.

### Migration Status

* MIG-001A PTrade Lifecycle: Completed
* MIG-001B Environment Validation: Completed
* MIG-001C Scheduler Validation: Completed
* MIG-002 Data Interface Migration: Completed

### Next Phase

* MIG-003 Indicator Migration
* Validate indicator calculations using live PTrade historical data.


## MIG-001C Scheduler Validation

Validated scheduled task framework.

Implemented:

run_daily(context, daily_heartbeat, time='14:50')

Verified:

- successful scheduler registration
- successful callback execution
- daily execution frequency
- correct execution time

Confirmed compatibility of
Guojin PTrade scheduling framework.

No trading logic changes.
No data interface changes.

## MIG-001B Environment Validation

Validated Guojin PTrade runtime environment.

Verified:

- context object
- context.portfolio object
- context.portfolio.cash
- context.portfolio.total_value
- context.portfolio.positions

Confirmed compatibility of core
account information access layer.

No strategy logic changes.
No execution logic changes.

## MIG-001A

Completed PTrade lifecycle integration.

Added:

- initialize(context)
- before_trading_start(context, data)
- after_trading_end(context, data)

Verified lifecycle callbacks execute correctly
within Guojin PTrade runtime.

No trading logic changes.
No data interface changes.
No execution interface changes.

### Documentation

Added Phase 9 PTrade Migration roadmap.

Introduced MIG-001:
PTrade Runtime Framework.

Migration review completed.

Identified:

- Functions already compatible with PTrade.
- Functions requiring future interface migration.
- Required PTrade lifecycle functions.
- Runtime integration architecture.

No strategy logic changes.
No production behavior changes.
Documentation update only.

## 2026-06-12

Stability Improvement

- Added floating-point tolerance handling in get_cash_weight()
- Residual cash allocations below 0.01% are rounded to zero
- Prevents creation of negligible CASH_ETF target positions caused by floating-point precision errors

Refactor

- Renamed calc_portfolio_volatility() to calc_weighted_average_volatility()
- Renamed portfolio_volatility variables to weighted_average_volatility
- Updated terminology to reflect weighted-average risk proxy rather than true covariance-based portfolio volatility

Project Status Update

- Current project focus changed from code review to PTrade migration
- Validation phase deferred until PTrade runtime becomes available

Documentation Update

- REVIEW-001 marked resolved after portfolio constraint interaction review
- REVIEW-002 marked resolved after FILTER-002 market exposure integration
- REVIEW-003 marked resolved after EXEC-002 cash ETF execution completion
- current_status updated to reflect no open review findings

### Fixed

RISK-002

- Integrated FILTER-002 market exposure into risk-adjusted portfolio sizing.
- Final allocation now incorporates:
  Target Weight × Market Exposure × Risk Scaling Factor.
- Fixed issue where market regime control was calculated but not applied.

EXEC-002

- Added automatic CASH_ETF allocation for residual cash.
- Cash weight is now translated into executable portfolio targets.
- Updated target symbol generation to include CASH_ETF.
- Eliminated unnecessary sell/rebuy cycles caused by missing CASH_ETF from target universe.

Architecture

- Completed end-to-end linkage:
  Market Filter → Risk Layer → Execution Layer.
- Portfolio exposure control now functions as originally designed.

## 2026-06-11

### Review

Performed focused code review on:

- RISK-001 Portfolio Risk Engine
- RISK-002 Risk Scaling Engine

Verified:

- risk budget calculation flow
- portfolio state consistency
- execution integration
- absence of recursive dependencies

Documented known design limitation:

- portfolio volatility currently uses weighted-average ETF volatility as a proxy risk estimate
- covariance-based portfolio volatility intentionally deferred for MVP

### Architecture Review

Reviewed interaction between PORT-002
(Position Constraints) and RISK-002
(Risk Scaling).

Findings:

- Current portfolio-level scaling does not
  violate position constraints.

- No code changes required.

- Future per-symbol risk allocation methods
  may require a second constraint enforcement
  pass after risk adjustment.

### Fixed

#### PORT-002 Portfolio Constraints

- Replaced single-pass maximum position constraint logic with iterative water-filling implementation.
- Added constraint convergence loop to prevent normalization from reintroducing weight-limit violations.
- Added protection against redistribution edge cases.
- Added portfolio constraint validation tests.
- Improved robustness of portfolio weight normalization workflow.

### Review Findings

Identified additional architecture review items:

- RISK-002 may override portfolio constraints after volatility adjustment.
- FILTER-002 market exposure is not yet integrated into final portfolio risk scaling.
- EXEC-002 cash allocation is not currently translated into Cash ETF orders.

## 2026-06-10

## [EXEC-002] Rebalance Engine

### Added

* Added `get_current_symbols()` to retrieve current portfolio holdings.
* Added `get_target_symbols()` to retrieve target portfolio holdings after risk adjustment.
* Added `sell_removed_positions()` to liquidate positions no longer included in the target portfolio.
* Added `rebalance_portfolio()` to execute target allocations.
* Added `rebalance()` as the main portfolio rebalancing workflow.
* Added EXEC-002 self-test validation.

### Changed

* Integrated ranking, portfolio construction, risk control, and execution layers into a complete rebalance pipeline.
* Rebalance process now supports automatic portfolio turnover and target-weight adjustment.

### Notes

* Current implementation uses the unified execution APIs introduced in EXEC-001.
* Cash allocation is handled through risk-adjusted portfolio weights.
* Actual order execution requires PTrade runtime.


## [EXEC-001] Order Mapping Layer

### Added

* Added unified execution abstraction layer.
* Implemented `order_target_value()` wrapper.
* Implemented `order_target_percent()` wrapper.
* Added centralized exception handling and execution error logging.
* Added execution layer self-test validation.

### Changed

* Strategy code can now use unified execution APIs instead of directly calling PTrade order functions.
* Established a broker-independent execution interface for future portability.

### Notes

* Current implementation maps orders to PTrade `order_value()` API.
* Local development environment uses execution stubs; actual order placement requires PTrade runtime.
* This module serves as the foundation for EXEC-002 Rebalance Engine.


## RISK-002 - Portfolio Risk Control

Completed implementation of portfolio risk control framework.

Added:

* Risk scaling factor calculation
* Portfolio exposure adjustment
* Dynamic risk budget control
* Risk-adjusted target weights
* Cash allocation calculation
* Risk control state classification

New Functions:

* get_risk_scaling_factor()
* get_risk_control_state()
* calc_risk_adjusted_weights()
* get_cash_weight()
* get_risk_control_summary()

Risk Control Logic:

* Low risk environment → Full exposure
* Normal risk environment → Slight exposure reduction
* High risk environment → Defensive scaling
* Extreme risk environment → Significant cash allocation

Validation:

* Risk scaling factor validated
* Cash allocation calculation validated
* Risk-adjusted weights generated successfully
* Risk control summary interface validated

Architecture:

Portfolio Layer
→ Risk Measurement (RISK-001)
→ Risk Control (RISK-002)
→ Execution Layer

Status: DONE
Phase 6 Risk Layer: COMPLETE

Next Task: EXEC-001 Order Generation


## RISK-001 - Portfolio Risk Engine

Completed implementation of portfolio risk measurement framework.

Added:

* Portfolio ATR calculation
* Portfolio volatility calculation
* Portfolio statistics interface
* Risk budget usage calculation
* Risk state classification (LOW / NORMAL / HIGH)

New Functions:

* calc_portfolio_atr()
* calc_portfolio_volatility()
* get_portfolio_statistics()
* calc_risk_budget_usage()
* get_risk_state()

Validation:

* Portfolio risk metrics generated successfully
* Risk budget utilization calculated correctly
* Risk statistics interface validated
* Risk state classification validated

Architecture:

Portfolio Layer
→ Risk Measurement (RISK-001)
→ Risk Control (RISK-002)
→ Execution Layer

Status: DONE
Next Task: RISK-002 Portfolio Risk Control


## PORT-002 - Portfolio Constraints

Completed implementation of portfolio constraint management.

Added:

* Portfolio weight normalization
* Maximum position size constraint
* Minimum position size constraint
* Excess weight redistribution
* Final target weight calculation pipeline

Validation:

* Portfolio weights normalized to 100%
* Position size limits enforced
* Minimum position threshold enforced
* Constraint layer integrated with PORT-001 output

Status: DONE
Phase 5 Portfolio Layer: COMPLETE

Next Task: RISK-001 Portfolio Risk Engine


## PORT-001 - Position Sizing

Completed implementation of portfolio position sizing module.

Added:

* ATR-based inverse volatility weighting
* Portfolio weight normalization
* Target weight calculation interface
* Validation framework

Validation:

* Weights sum to 100%
* All weights remain positive
* Empty portfolio handled correctly

Status: DONE
Next Task: PORT-002 Portfolio Constraints


## [Architecture Review] - After Phase 4 Completion

### Fixed

- BUG-004:
  Standardized account equity access interface.
  Corrected context parameter handling.

- BUG-005:
  Standardized account cash access interface.
  Corrected context parameter handling.

### Added

- validate_ranking_pipeline()
  End-to-end validation for:

  Market Data
  → Indicators
  → Market Filters
  → Final Score
  → ETF Selection

### Reviewed

- Naming consistency
- Indicator interface consistency
- Return value conventions
- Validation coverage
- PTrade compatibility
- Documentation synchronization

### Deferred

- Ranking score cache optimization.
- Cache implementation postponed until Portfolio Layer development.

### Notes

- Local execution of ranking pipeline validation remains unavailable because required PTrade runtime APIs are not present outside the production environment.

## 2026-06-09

## RANK-002 ETF Selection

Implemented ETF selection and ranking layer.

Added:

* ETF trend filter framework.
* Long-term trend validation using MA200.
* ETF eligibility screening logic.
* Final ETF ranking based on weighted score.
* Top-N ETF selection process.
* Selected ETF list generation.
* Ranking and selection validation tests.
* Integration into project validation pipeline.

Documentation updated:

* task_list.md
* current_status.md
* README.md

Notes:

* RANK-002 consumes outputs from:

  * FILTER-001 Market Breadth
  * FILTER-002 Market Exposure
  * RANK-001 Final Score
* Applies long-term trend filtering before ranking.
* Produces final ETF candidate list for portfolio construction.
* Completes Phase 4 - Ranking Layer.

Architecture milestone:

The system now supports a complete ETF selection workflow:

Data Access
→ Indicators
→ Market Filter
→ Ranking
→ ETF Selection


## RANK-001 Final Score

Implemented ETF final ranking score framework.

Added:

* Final score calculation layer.
* Configurable ranking weights:

  * Momentum Score Weight
  * Quality Score Weight
  * Liquidity Score Weight
* Weighted scoring model:

  * 70% Momentum
  * 20% Quality
  * 10% Liquidity
* `calc_final_score()` function.
* ETF ranking infrastructure.
* Ranking validation tests.
* Integration into project validation pipeline.

Documentation updated:

* task_list.md
* current_status.md
* README.md

Notes:

* RANK-001 consumes outputs from:

  * IND-003 Momentum Score
  * IND-004 Quality Score
  * IND-005 Liquidity Score
* Provides unified ETF ranking score for portfolio selection.
* Establishes the core ranking mechanism used by RANK-002 ETF Selection.


## FILTER-002 Market Exposure

Implemented market exposure control layer.

Added:

* Market exposure mapping framework.
* Exposure adjustment based on market breadth score.
* Market score to exposure conversion logic:

  * Score 0 → 0.00
  * Score 1 → 0.50
  * Score 2 → 0.80
  * Score 3 → 1.00
* `MARKET_EXPOSURE_MAP` parameter definition.
* `calc_market_exposure()` function.
* FILTER-002 validation tests.
* Integration into project validation pipeline.

Documentation updated:

* task_list.md
* current_status.md
* README.md

Notes:

* FILTER-002 consumes FILTER-001 output.
* Provides portfolio-level exposure target for future position sizing modules.
* Completes Phase 3 - Market Filter.


### Added

#### FILTER-001 Market Breadth

Implemented institutional market breadth filter layer.

Features added:

* Added market breadth scoring framework.
* Added configurable market index universe:

  * CSI 300 ETF (510300)
  * CSI 500 ETF (510500)
  * CSI 1000 ETF (512100)
* Added moving average calculation utility:

  * MA50
  * MA150
  * MA250
* Added bull trend detection logic:

  * Close > MA50 > MA150 > MA250
* Added `calc_market_score()` function.
* Market score ranges from 0 to 3.
* Added validation and self-test framework for FILTER-001.
* Integrated FILTER-001 into project validation sequence.

### Documentation

* Updated task_list.md:

  * FILTER-001 marked as DONE.
  * FILTER-002 marked as IN PROGRESS.
* Updated current_status.md:

  * Advanced progress to Phase 3 Market Filter.
* Updated README.md:

  * Added Market Breadth filter documentation.
  * Added market regime evaluation workflow.
  * Added market score description and usage notes.


## 2026-06-08

## [FIX-001] Infrastructure Cleanup

### Added

* Added PTrade API stub:

  * `get_history()`

* Added logging interfaces:

  * `log_info()`
  * `log_warning()`
  * `log_error()`

* Added standardized account APIs:

  * `get_equity()`
  * `get_cash()`

### Changed

* Normalized DATA-004 account access layer interface naming.
* Unified error handling through logging functions.
* Improved local development compatibility and static analysis support.

### Fixed

* Resolved undefined symbol warnings for `get_history()`.
* Resolved undefined symbol warnings for `log_error()`.
* Removed all known VSCode code-analysis errors.

### Notes

This update introduces no strategy functionality changes and no trading logic modifications. It is a development infrastructure improvement only.


## [IND-006] ATR20 Indicator

### Added

* Added ATR20 indicator module (IND-006).
* Added `ATR_LOOKBACK` parameter (20 trading days).
* Added True Range (TR) calculation framework.
* Added `calc_true_range()` helper function.
* Added ATR20 calculation based on 20-day average True Range.
* Added `calc_atr()` indicator function.
* Added ATR percentage calculation (`ATR / Close`).
* Added `calc_atr_percent()` helper function.
* Added IND-006 validation test.
* Added runtime validation hook.

### Design Notes

* ATR is calculated using the classic True Range methodology.
* ATR measures absolute market volatility.
* ATR Percentage provides a normalized volatility measure across ETFs with different price levels.
* ATR will be reused by future risk management and execution modules.
* Implementation follows Institutional China ETF Trend Following Portfolio v4.0 specification.

### Phase 2 Completed

Indicator Layer has been fully implemented.

Completed indicators:

* IND-001 Return Calculation
* IND-002 Volatility Calculation
* IND-003 Relative Strength Score
* IND-004 Trend Quality Score
* IND-005 Liquidity Score
* IND-006 ATR20

Indicator Layer now provides:

* Return metrics
* Volatility metrics
* Momentum ranking
* Trend quality ranking
* Liquidity ranking
* ATR-based volatility measurement

### Project Status

Completed Phases:

* Phase 1 — Data Layer ✓
* Phase 2 — Indicator Layer ✓

Next Phase:

* Phase 3 — Risk Layer

Next Task:

* RISK-001 Portfolio Risk Engine


## [IND-005] Liquidity Score

### Added

* Added liquidity indicator layer (IND-005).
* Added `LIQUIDITY_LOOKBACK` parameter (60 trading days).
* Added ADV60 (Average Daily Turnover) calculation.
* Added `calc_adv60()` helper function.
* Added cross-sectional liquidity ranking framework.
* Added `calc_liquidity_score()` indicator function.
* Reused percentile ranking infrastructure from IND-003.
* Added IND-005 validation test.
* Added runtime validation hook.

### Design Notes

* Liquidity is measured using 60-day average daily turnover.
* Cross-sectional percentile ranking is used for score normalization.
* Higher-turnover ETFs receive higher liquidity scores.
* Implementation follows Institutional China ETF Trend Following Portfolio v4.0 specification.

### Project Status

Completed:

* IND-001 Return Calculation
* IND-002 Volatility Calculation
* IND-003 Relative Strength Score
* IND-004 Trend Quality Score
* IND-005 Liquidity Score

Next:

* IND-006 ATR20


## [IND-004] Trend Quality Indicator

### Added

* Implemented Trend Quality indicator layer (IND-004).

* Added `QUALITY_LOOKBACK = 120` configuration parameter.

* Added `calc_trend_quality_raw()` function.

* Added log-price linear regression based trend quality calculation.

* Added slope estimation from least-squares regression.

* Added R² (coefficient of determination) calculation for trend consistency measurement.

* Added raw quality metric:

  Quality Raw = Slope × R²

* Added `calc_quality_score()` function.

* Added cross-sectional percentile ranking of trend quality across ETF universe.

* Reused IND-003 percentile ranking framework for score normalization.

* Added IND-004 validation test `_test_quality_score()`.

* Added runtime validation hooks in main execution block.

### Design Notes

* Trend Quality evaluates both trend strength and trend smoothness.
* Positive and persistent trends receive higher scores.
* Noisy or unstable trends are penalized through lower R² values.
* Downtrending assets naturally rank lower due to negative regression slope.
* Implementation follows the Institutional China ETF Trend Following Portfolio v4.0 specification.

### Project Status

* Phase 2 Indicator Layer progress updated.

* Completed indicators:

  * IND-001 Return Calculation
  * IND-002 Volatility Calculation
  * IND-003 Relative Strength Score
  * IND-004 Trend Quality Score

* Next planned task:

  * IND-005 Liquidity Score


## 2026-06-07

## [IND-003] Momentum Score Engine

### Added

* Implemented cross-sectional momentum ranking framework.
* Added Risk Adjusted Momentum calculation:

  * Momentum20 = Return20 / Volatility60
  * Momentum60 = Return60 / Volatility60
  * Momentum120 = Return120 / Volatility60
  * Momentum250 = Return250 / Volatility60
* Added percentile ranking function for ETF universe normalization.
* Added weighted momentum aggregation model:

  * 5% × 20-day momentum rank
  * 15% × 60-day momentum rank
  * 30% × 120-day momentum rank
  * 50% × 250-day momentum rank
* Added final Momentum Score output normalized to the range [0, 1].
* Added defensive handling for:

  * Missing return data
  * Missing volatility data
  * Zero volatility conditions
  * Small cross-sectional sample sizes
* Added IND-003 self-test validation.

### Architecture

* Established the portfolio momentum ranking layer.
* Created the primary ranking signal used by later portfolio selection modules.
* Prepared dependency foundation for:

  * IND-004 Trend Filter
  * IND-005 Quality Score
  * IND-006 Final Composite Score
  * Future ranking and allocation engines

### Status

* IND-003 marked as COMPLETE.
* Phase 2 Indicator Layer progress:

  * IND-001 Return Calculation ✔
  * IND-002 Volatility Calculation ✔
  * IND-003 Momentum Score ✔
  * IND-004 Trend Filter ⏳
  * IND-005 Quality Score ⏳
  * IND-006 Final Score ⏳


## Added - IND-002 Volatility Calculation

### Overview

Implemented IND-002 Volatility Calculation as part of Phase 2 (Indicator Layer).

This module provides annualized volatility measurement for ETF ranking and risk-adjusted momentum calculations.

### Implementation

Added:

* `calc_volatility(symbol, lookback=60)`

Features:

* Retrieves historical close prices using Data Access Layer
* Calculates daily percentage returns
* Computes sample standard deviation of returns
* Annualizes volatility using √252 scaling factor
* Handles insufficient data gracefully
* Returns `None` when calculation cannot be completed

Formula:

Annualized Volatility = Std(Daily Returns) × √252

### Validation

Validation completed successfully.

Verified:

* Return series generation
* Volatility calculation logic
* Annualization process
* Error handling for insufficient data

### Architecture Impact

IND-002 completes the volatility component of the Indicator Layer and provides a core dependency for:

* IND-003 Momentum Score
* IND-006 Asset Ranking

### Project Status

Completed Tasks:

* DATA-001 Configuration Layer
* DATA-002 Data Access Layer
* DATA-003 PTrade Integration Layer
* DATA-004 Account Access Layer
* STATE-001 State Management Layer
* IND-001 Return Calculation
* IND-002 Volatility Calculation

Phase 2 Progress:

* IND-001 Return Calculation — DONE
* IND-002 Volatility Calculation — DONE
* IND-003 Momentum Score — NOT STARTED
* IND-004 Trend Filter — NOT STARTED
* IND-005 ATR Calculation — NOT STARTED
* IND-006 Ranking Engine — NOT STARTED


### IND-001 Return Calculation

Added:

* `calc_return()`
* `return_20()`
* `return_60()`
* `return_120()`
* `return_250()`

Implemented:

* 20-day return calculation
* 60-day return calculation
* 120-day return calculation
* 250-day return calculation

Configuration update:

* Removed `MOMENTUM_LOOKBACK`
* Added `RETURN_LOOKBACKS`

Validation update:

* Added return lookback validation
* Added lookback ordering validation

Status:

* IND-001 completed


[2026-06-06]

## [DATA-004] Portfolio Access Layer

### Added

Implemented DATA-004 Portfolio Access Layer.

Provides a unified interface for accessing portfolio and position information from the PTrade runtime environment.

### Features

Added portfolio-level access functions:

* `get_total_equity()`
* `get_available_cash()`
* `get_position_value()`

Added position-level access functions:

* `get_positions()`
* `get_position()`
* `has_position()`
* `get_position_amount()`
* `get_available_amount()`
* `get_position_cost()`
* `get_position_price()`
* `get_position_market_value()`

Added validation function:

* `validate_portfolio_access_layer()`

### Architecture

The layer abstracts direct access to:

* `context.portfolio`
* `context.portfolio.positions`
* PTrade `Position` objects

This prevents upper layers from depending on PTrade-specific APIs.

### Dependencies

Requires:

* DATA-003 Data Access Layer
* STATE-001 Strategy State

### Enables

Provides required infrastructure for:

* RISK-001 Portfolio Risk Engine
* RISK-002 Position Sizing Engine
* EXEC-001 Rebalance Engine
* EXEC-002 Order Execution Layer

Added

DATA-002 Configuration Management
Implemented configuration management module.
Added strategy parameter definitions.
Added configuration validation.
Refactored configuration architecture from CONFIG dictionary to constant-based configuration model.
DATA-003 Data Access Layer
Implemented unified market data access layer.
Added close/high/low/volume/turnover retrieval functions.
Added historical data validation utilities.
Added ETF data availability checks.
Added valid ETF universe filtering.
Maintenance
Updated self-test framework.
Disabled DATA-003 local validation outside PTrade runtime.
Verified:
DATA-001 PASS
DATA-002 PASS
STATE-001 PASS

STATE-001 Strategy State Management

Implemented strategy state management framework:

entry_price tracking
entry_date tracking
stop_price tracking
highest_close tracking
state initialization
state validation
state cleanup after exit
PROJECT_RULES.md

Added project-level architecture constraints:

Single File Architecture
No package structure
No multi-file design
No cross-file imports
All implementations must reside in china_etf_trend_strategy.py

Changed
task_list.md

Updated task status:

STATE-001 → DONE
current_status.md

Updated project progress:

STATE-001 completed

Notes

Current architecture constraint:

PTrade platform requires Single File Architecture.

All future implementations must be integrated into:

china_etf_trend_strategy.py

## Added

### DATA-002 Configuration Management

新增统一CONFIG管理系统

包含：

- Data Layer Parameters
- Market Filter Parameters
- Momentum Parameters
- Quality Parameters
- Liquidity Parameters
- Portfolio Parameters
- Risk Parameters
- Execution Parameters

实现：

Single Source of Truth

所有参数统一由CONFIG管理。

---

Added

DATA-001 Asset Definition Layer

Components:
- CASH_ETF
- RISK_ETFS
- ETF_UNIVERSE
- ETF_CATEGORY_MAP
- ETF_NAME_MAP
- ASSET_CLASS_MAP
- validate_universe()

Status:
Completed

# [v4.0] - 2026-06-05

## Added

### Architecture

* 新增 Data Specification
* 新增 State Management
* 新增 Error Handling
* 新增 Logging Framework
* 新增 Validation Framework
* 新增 Development Rules

### Project Management

* 新增 task_list.md
* 新增 current_status.md
* 新增 changelog.md

### Risk Management

* 新增组合最大回撤控制机制
* 新增防御模式（Defensive Mode）

### State Management

新增：

* entry_price
* entry_date
* stop_price
* highest_close

统一状态管理结构。

---

## Changed

### Momentum Model

旧版本：

126日动量

* Skip 21 Days

新版本：

* 250日动量（50%）
* 120日动量（30%）
* 60日动量（15%）
* 20日动量（5%）

统一采用多周期动量模型。

### Quality Score

旧版本：

0.7 × Slope
+
0.3 × R²

新版本：

Standardized(Slope × R²)

减少参数数量。

### Final Score

旧版本：

0.70 Momentum
+
0.30 Quality

新版本：

0.70 Momentum
+
0.20 Quality
+
0.10 Liquidity

加入流动性评分。

### Parameter System

统一迁移至：

CONFIG

集中管理。

---

## Removed

### Parameter Conflicts

删除：

* Momentum Window = 126
* Skip Recent Days = 21
* Slope Weight
* R² Weight

避免重复定义。

---

## Fixed

### Formula Consistency

修复：

* Momentum模型冲突
* Quality Score冲突
* Final Score冲突

统一文档定义。

---

# [v3.0] - Historical Version

## Added

### ETF Universe

固定：

20只风险资产ETF
+
1只现金ETF

### Liquidity Score

引入流动性评分体系。

### PTrade Architecture

引入：

* 单脚本架构
* API映射层
* PTrade兼容原则

---

# [v2.0] - Historical Version

## Added

### Trend Following Framework

建立：

* 市场过滤
* 动量排序
* 趋势质量
* 风险控制

核心框架。

---

# [v1.0] - Historical Version

## Initial Release

项目首次建立。

核心目标：

构建适用于中国A股ETF市场的趋势跟踪轮动系统。
