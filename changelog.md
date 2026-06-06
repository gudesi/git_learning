# Changelog

All notable changes to this project will be documented in this file.

Format:

* Added
* Changed
* Removed
* Fixed

[2026-06-06]

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

Added

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
