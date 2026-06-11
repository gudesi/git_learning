# Institutional China ETF Trend Following Portfolio

## Project Overview

机构级中国A股ETF趋势跟踪系统。

目标：

- Long Only
- ETF Rotation
- Trend Following
- PTrade Compatible

---

## Documentation

report.md
系统设计文档

task_list.md
开发任务列表

current_status.md
当前开发状态

changelog.md
项目变更历史

PROJECT_RULES.md
项目规则
---

## Current Progress

Current Phase:
Phase 8 - Execution Layer completed

Current Task:
code review before continue
---

## Development Rules

- PTrade优先
- 单脚本架构
- CONFIG统一参数管理
- 回测与实盘共用代码

### Risk Model Notes

Current implementation uses a simplified portfolio risk model.

Portfolio volatility is estimated as:

weighted average ETF volatility

rather than a covariance-based portfolio volatility model.

This approximation is intentional and sufficient for the current MVP because:

- ETF universe size is small
- Risk control is used for exposure scaling only
- Simplicity is preferred for PTrade deployment

Future versions may introduce covariance-based portfolio risk estimation if additional precision is required.