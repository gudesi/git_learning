# Current Status

Project:
Institutional China ETF Trend Following Portfolio v4.0

Last Updated:
2026-06-14

Current Phase:
# Phase 8.5 - PTrade Migration

Current Focus

## MIG-005B Filter Integration

Overall Progress:
28 / 38 Tasks Completed

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

# Phase 8.5 - PTrade Migration

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

| MIG-005B | NOT STARTED |
| MIG-005C | NOT STARTED |
| MIG-005D | NOT STARTED |
| MIG-005E | NOT STARTED |
| MIG-005F | NOT STARTED |
| MIG-005G | NOT STARTED |
| MIG-006 | NOT STARTED |
| MIG-007 | NOT STARTED |
| MIG-008 | NOT STARTED |

Progress:
7 / 16

Objective:

Integrate strategy engine into PTrade lifecycle
without modifying strategy logic.

# Phase 9 - Validation

| Task ID  | Status      |
| -------- | ----------- |
| TEST-001 | NOT STARTED |
| TEST-002 | NOT STARTED |
| TEST-003 | NOT STARTED |
| TEST-004 | NOT STARTED |

Progress:
0 / 4

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


