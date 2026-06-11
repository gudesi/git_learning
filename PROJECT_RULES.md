# PROJECT RULES

## RULE-001

Single File Architecture

所有代码最终必须存在于：

china_etf_trend_strategy.py

禁止：

- 多文件架构
- package结构
- 跨文件import

原因：

PTrade平台限制

## RULE-002(Constraint Enforcement Rule)

Current architecture:

Ranking
    ↓
Portfolio Construction
    ↓
Risk Adjustment
    ↓
Execution

RISK-002 currently performs only
portfolio-level scaling.

Portfolio constraints remain valid
after scaling.

If future risk modules introduce
per-symbol weight modifications
(volatility targeting, ATR targeting,
risk parity, etc.), constraint
enforcement must be executed again
after risk adjustment.

This requirement has been verified
during architecture review.