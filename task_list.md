# P0 - Execution Layer Stabilization
Status: Completed

EXEC-001 Cash Check
Status: Completed

EXEC-002 Commission Buffer
Status: Completed

EXEC-003 Sell First
Status: Completed

EXEC-004 Scaled Buy
Status: Completed

EXEC-005 Threshold Bug Fix
Status: Completed

验证：

✓ 长周期回测通过
  (2024-06-01 ~ 2026-06-01)

✓ REMOVE 成功清仓

✓ 无 ORDER_TARGET_PERCENT_EXCEPTION

✓ 无 UnboundLocalError

✓ 持仓正确更新

# P1 - Portfolio Exposure Reconstruction
Status: In Progress

目标：

定位策略长期低收益原因。

当前两年回测：

2024-06-01 ~ 2026-06-01

累计收益：

5.29%

已完成：

## P1-A Exposure Audit
Status: Completed

审计结果：

AUDIT_DAYS=400

AVG_CASH_WEIGHT=0.8000

CASH_GT_50_PCT=71.25%

CASH_GT_80_PCT=52.25%

AVG_RISK_FACTOR=0.5019

AVG_MARKET_FACTOR=0.3962

AVG_FINAL_FACTOR=0.2000

结论：

策略长期处于过度防御状态。

风险资产暴露通常仅为：

10% ~ 20%

现金仓长期占：

80%+

怀疑收益不足主要来自：

Market Exposure Engine
+
Risk Budget Engine

## P1-B Risk Budget Engine Audit
Status: Pending

目标：

验证 calc_risk_budget_usage()

是否正确计算组合风险。

当前怀疑：

weighted_average_volatility()

计算的是：

资产平均波动率

而不是：

组合实际波动率

可能导致：

风险引擎长期误判为：

DEFENSIVE_EXPOSURE

验证内容：

PORTFOLIO_VOL

RISK_USAGE

RISK_FACTOR

完成标准：

确认风险预算逻辑是否存在结构性缺陷。

## P1-C Market Exposure Review
Status: Pending

目标：

评估市场过滤器是否过于保守。

当前配置：

50 / 100 / 200 MA

市场指数：

510300
510500
512100

暴露映射：

0 -> 0.00
1 -> 0.50
2 -> 0.80
3 -> 1.00

审计结果：

AVG_MARKET_FACTOR
长期仅：

0.04 ~ 0.40

验证内容：

Market Score 分布

各 Score 出现频率

长期平均暴露

完成标准：

确认市场过滤器是否过度压制仓位。

## P1-D Cash Allocation Redesign
Status: Pending

目标：

重新定义 511880 的角色。

原则：

511880 仅作为现金停泊位。

不参与风险资产竞争。

避免现金仓成为主要持仓。

依赖：

P1-B
P1-C

# P2 - 收缩资产池	优先保留宽基ETF和少数长期有效的赛道ETF；对长期净贡献为负的品种做样本外验证后再决定是否剔除。
       优化打分函数	降低“质量/流动性”在当前模型中的权重，加入趋势持续性、回撤惩罚或斜率稳定性，提升信号的可交易性。
# P3 - 做 walk-forward	用滚动窗口重新训练/验证权重，不要依赖整段样本的固定参数直接外推到未来。

最重要的判断：这不是一个“再调一点参数就能从 7.65% 变成 15%”的问题。它更像是一个需要先修执行、再收缩资产池、最后重做信号工程的系统性重构问题。