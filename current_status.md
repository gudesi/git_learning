# Current Status

Project:
Institutional China ETF Trend Following Portfolio v4.0

Last Updated:
2026-06-17

Current Phase:
# Phase 9 - PTrade Migration

Current Focus

## PERF-003 Ranking Cache(Indicator Cache Optimization?)

Objective:

Reduce repeated historical data retrieval and indicator recomputation by introducing cache support for core indicator functions.

Overall Progress:
36 / 42 Tasks Completed

---

# Phase 1 - Foundation Layer

| Task ID  | Status      |
| -------- | ----------- |
| DATA-001 | DONE |
| DATA-002 | DONE |
| DATA-003 | DONE |
| DATA-004 | DONE |

Progress:
4 / 4

---

# Phase 2 - Indicator Layer

| Task ID | Status      |
| ------- | ----------- |
| IND-001 | DONE |
| IND-002 | DONE |
| IND-003 | DONE |
| IND-004 | DONE |
| IND-005 | DONE |
| IND-006 | DONE |

Progress:
6 / 6

### FIX-001 Infrastructure Cleanup

Completed development cleanup prior to Market Filter implementation.

Changes:

- Added get_history() PTrade stub
- Added log_info(), log_warning(), log_error()
- Added standardized account APIs:
  - get_equity()
  - get_cash()
- Removed all known VSCode undefined symbol errors

Impact:

- No strategy logic changed
- No performance impact
- Improves maintainability and local development experience

Status: Done
---

# Phase 3 - Market Filter

| Task ID    | Status      |
| ---------- | ----------- |
| FILTER-001 | DONE |
| FILTER-002 | DONE |

Progress:
2 / 2

---

# Phase 4 - Ranking Layer

| Task ID  | Status      |
| -------- | ----------- |
| RANK-001 | DONE |
| RANK-002 | DONE |

Progress:
2 / 2

## Post-Phase-4 Review

Architecture review completed.

Completed:
- Fixed BUG-004: account equity interface consistency.
- Fixed BUG-005: account cash interface consistency.
- Added validate_ranking_pipeline().
- Verified naming consistency.
- Verified indicator interface consistency.
- Verified return value conventions.
- Verified validation coverage.
- Verified PTrade compatibility.
- Verified documentation synchronization.

Deferred:
- Ranking score cache optimization.
- Cache design review after PORT-001 completion.

Known Limitation:
- Ranking pipeline validation cannot execute in local environment because PTrade runtime APIs are unavailable.

System now has its first complete decision pipeline:

Market Data
→ Indicators
→ Market Filters
→ Final Score
→ ETF Selection

Architecture review completed.
Ready for PORT-001.
---

# Phase 5 - Portfolio Layer

| Task ID  | Status      |
| -------- | ----------- |
| PORT-001 | DONE |
| PORT-002 | Functional(Not Yet Production Safe) |

Progress:
2 / 2

Latest Review Findings

Resolved:
- PORT-002 weight constraint redistribution bug.
- Portfolio constraint normalization edge cases.

Pending Review:
- RISK-002 risk-adjusted weighting may bypass portfolio constraints.
- FILTER-002 market exposure not yet integrated into risk layer.
- EXEC-002 cash ETF execution logic.

## Architecture Notes

### PORT-002 Constraint Enforcement

A post-implementation architecture review was conducted
to verify whether PORT-002 position constraints could be
invalidated by RISK-002 risk scaling.

Current conclusion:

- RISK-002 applies uniform portfolio scaling.
- Relative position weights remain unchanged.
- PORT-002 maximum/minimum position constraints remain valid.

No code changes required.

Future warning:

If RISK-002 evolves into per-symbol risk adjustment
(e.g. ATR targeting, volatility targeting, risk parity),
position constraints should be re-applied after risk
adjustment to ensure enforcement.
---

# Phase 6 - Risk Layer

| Task ID  | Status      |
| -------- | ----------- |
| RISK-001 | DONE |
| RISK-002 | DONE |

Progress:
2 / 2

### Risk Layer Review (2026-06-11)

RISK-001 and RISK-002 completed code review.

Review findings:

- No recursive dependency detected.
- Risk scaling pipeline verified.
- Portfolio state synchronization verified.
- PTrade execution flow verified.

Known limitation:

- Portfolio volatility currently uses weighted-average ETF volatility as a proxy estimate.
- Covariance-based portfolio volatility is intentionally deferred and is not required for current MVP implementation.

RISK-002 Status

Completed:
- Portfolio volatility estimation
- Risk budget usage calculation
- Risk scaling factor generation
- Market exposure integration

Final position sizing:

Final Weight
=
Target Weight
× Market Exposure
× Risk Scaling Factor

This ensures that both market regime risk and portfolio risk constraints participate in allocation decisions.
---

# Phase 7 - State Management

| Task ID   | Status      |
| --------- | ----------- |
| STATE-001 | DONE |

Progress:
1 / 1

---

# Phase 8 - Execution Layer

| Task ID  | Status      |
| -------- | ----------- |
| EXEC-001 | DONE |
| EXEC-002 | DONE |

Progress:
2 / 2

EXEC-002 Status

Completed:
- Target portfolio construction
- Removed-position liquidation
- Cash ETF allocation support

Residual cash is automatically allocated to CASH_ETF.

Target symbol universe now includes CASH_ETF when cash allocation exists, preventing unnecessary sell/rebuy operations during rebalancing.

---

## Validation Phase Review Status

Resolved

- BUG-001 DATA-003 runtime validation issue
- BUG-002 DATA-004 API naming consistency
- BUG-003 PORT-002 max-position redistribution bug

Resolved

- REVIEW-001 RISK-002 portfolio constraint interaction reviewed
- REVIEW-002 FILTER-002 integrated into risk engine
- REVIEW-003 EXEC-002 cash ETF execution completed

Open

None

# Phase 9 - PTrade Migration

| Task ID | Status |
|----------|----------|
| MIG-001A | DONE |
| MIG-001B | DONE |
| MIG-001C | DONE |
| MIG-002 | DONE |
| MIG-003 | DONE |
| MIG-004 | DONE |

Migration Layer

Status:
Frozen

Review Result:

PASS

Completed:

MIG-001 Lifecycle
MIG-002 Data Interface
MIG-003 Portfolio Mapping
MIG-004 Order Mapping

Migration Layer v1.0 Frozen

No further modifications planned.

| MIG-005A | DONE |

Validated:
- Historical data wrapper
- Return indicators
- Volatility indicators
- Momentum indicators
- Trend quality indicators
- Liquidity indicators
- ATR indicators

Notes:
- PTrade requires explicit exchange suffixes
  (.SS / .SZ)

- Cross-sectional ranking now produces
  non-neutral scores.

| MIG-005B | DONE |

Validated:

✓ MA50 calculation
✓ MA150 calculation
✓ MA250 calculation
✓ Bull trend detection
✓ Market breadth scoring
✓ Market exposure mapping
✓ PTrade historical data access

Result:

FILTER-001 operational
FILTER-002 operational

| MIG-005C | DONE |

Performance Observation

MIG-005C validation completed successfully.

Observed:

Ranking pipeline introduces significant runtime overhead due to repeated indicator calculations across ETF universe.

Impact:

Backtest runtime increased from approximately 1 minute to approximately 9 minutes.

Status:

Accepted for migration phase.

Optimization deferred until post-MIG-005F performance review.


| MIG-005D | DONE |
| MIG-005E | DONE |
| MIG-005F | DONE |
| MIG-005G | DONE |

Post-Migration Performance Optimization

Status:
IN PROGRESS

Reason:

Migration review completed successfully.

No API compatibility issues detected.

Performance review identified:

- Excessive historical data retrieval
- Repeated indicator calculations
- Repeated ranking calculations
- Repeated portfolio construction calculations
- Missing cache layer from original architecture

Optimization Plan:

PERF-001 Cache Infrastructure     DONE
PERF-002 History Data Cache       DONE

Performance Review Status


REVIEW-004
Status: Resolved

Target weight pipeline deduplicated.

Introduced:

- get_target_weights()

Result:

- target portfolio construction executed once per cycle
- repeated PORT-001 / PORT-002 execution removed


REVIEW-005
Status: Deferred

Portfolio statistics caching reviewed.

Conclusion:

- existing history cache already removes major data access overhead
- additional statistics cache expected to provide limited benefit

Deferred until future profiling identifies bottleneck.


REVIEW-006
Status: Resolved

Risk pipeline deduplicated.

Refactored:

- get_cash_weight()
- get_target_symbols()
- sell_removed_positions()
- rebalance_portfolio()

Result:

- calc_risk_adjusted_weights() centralized
- repeated risk pipeline execution removed
- rebalance workflow simplified

PERF-003 Ranking Cache            DONE

Status: Completed

Ranking Cache implemented.

Validation:
- build_ranking_table() executes once per trading day.
- Cache cleared by PERF-001 daily.
- Backtest verification passed.

REVIEW-007
Symbol Format Consistency

Status: Completed

Issue:
Current positions use XSHG/XSHE.
Strategy universe uses SS/SZ.

Impact:
sell_removed_positions()
generates unnecessary sell-and-buy cycles.

Priority:
High

Symbol format normalization added.

Validation:
- XSHG -> SS
- XSHE -> SZ

Result:
- sell_removed_positions() no longer generates
  repeated sell-and-buy cycles.

Backtest passed.

REVIEW-008
Status: Deferred

Execution order sequencing may impact capital efficiency.

No functional defect.

PERF-004 Portfolio Cache          NOT STARTED
PERF-005 Performance Validation   NOT STARTED

Expected Result:

Restore near pre-migration runtime while preserving
all migrated functionality.

| MIG-006 | NOT STARTED |
| MIG-007 | NOT STARTED |
| MIG-008 | NOT STARTED |

Progress:
14 / 21

Objective:

Integrate strategy engine into PTrade lifecycle
without modifying strategy logic.

---

# Open Bugs

| Bug ID  | Status |
| ------- | ------ |
| BUG-001 | OPEN   |
| BUG-002 | OPEN   |
| BUG-003 | OPEN   |


# Completion Rules

NOT STARTED

尚未开始开发

IN PROGRESS

正在开发

DONE

已完成并通过验证

BLOCKED

存在依赖或问题无法继续


