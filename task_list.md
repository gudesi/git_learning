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

Validation:

✓ Long-term backtest passed
(2024-06-01 ~ 2026-06-01)

✓ REMOVE successfully liquidates positions

✓ No ORDER_TARGET_PERCENT_EXCEPTION

✓ No UnboundLocalError

✓ Positions update correctly

---

# P1 - Portfolio Exposure Reconstruction

Status: Completed

Goal:

Identify root cause of chronic underperformance.

Original Backtest
(2024-06-01 ~ 2026-06-01)

Return:
5.29%

---

## P1-A Exposure Audit

Status: Completed

Audit Summary:

AUDIT_DAYS=400

AVG_CASH_WEIGHT=0.8000

CASH_GT_50_PCT=71.25%

CASH_GT_80_PCT=52.25%

AVG_RISK_FACTOR=0.5019

AVG_MARKET_FACTOR=0.3962

AVG_FINAL_FACTOR=0.2000

Conclusion:

Strategy remained in a highly defensive state.

Average risk exposure was only 20%.

Cash allocation averaged 80%.

---

## P1-B Risk Budget Engine Audit

Status: Completed

Findings:

1. Portfolio volatility uses weighted-average volatility rather than true covariance-based portfolio volatility.

2. TARGET_PORTFOLIO_RISK=10% was likely too conservative.

3. Risk Budget Engine reduced exposure materially.

4. Market Exposure Engine remained the dominant source of underexposure.

---

## P1-C Market Exposure Review

Status: Completed

Findings:

1. AVG_MARKET_FACTOR=0.3962

2. Market Exposure Engine was the primary source of chronic underexposure.

3. MA50 > MA100 > MA200 trend definition was excessively strict.

4. Trend filtering existed at both market level and ETF level.

---

## P1-D Market Filter Redesign

Status: Completed

Backtest Validation:

Replace:

def calc_market_exposure()

with:

return 1.0

Result:

Annual Return:
2.70% -> 10.13%

Sharpe:
-0.17 -> 0.55

Max Drawdown:
5.28% -> 8.79%

Conclusion:

Market Exposure Engine duplicated ETF trend filtering and significantly reduced performance.

Decision:

Remove Market Exposure Engine.

Final Implementation:

def calc_market_exposure():
return 1.0

---

## P1-E Risk Budget Engine Review

Status: Completed

Sensitivity Test:

Target Risk = 10%

Annual Return:
10.13%

Sharpe:
0.55

Max DD:
8.79%

---

Target Risk = 15%

Annual Return:
13.65%

Sharpe:
0.79

Max DD:
8.82%

---

Target Risk = 20%

Annual Return:
13.61%

Sharpe:
0.70

Max DD:
9.75%

Conclusion:

TARGET_PORTFOLIO_RISK=10%
is too conservative.

TARGET_PORTFOLIO_RISK=15%
provides the best risk-adjusted performance.

Increasing target risk beyond 15%
does not improve returns and increases drawdown.

Decision:

TARGET_PORTFOLIO_RISK = 0.15

---

P1 Final Result

Original Strategy:

Annual Return:
2.70%

Sharpe:
-0.17

Max DD:
5.28%

---

After P1 Reconstruction:

Annual Return:
13.65%

Sharpe:
0.79

Max DD:
8.82%

Conclusion:

The primary cause of underperformance was excessive exposure suppression.

P1 successfully resolved the exposure bottleneck.

---
# P2 - ETF Selection Audit

Status: Completed

Objective:

Identify ETFs with persistent negative contribution and determine whether they should remain in the universe.

Completed Work:

## P2-A ETF Attribution Analysis

Completed

Analyzed:

* Trade records
* Holding records
* ETF-level contribution
* Win rate
* Profit/loss ratio

Key Findings:

Negative contributors:

* 588000.SS
* 512660.SS
* 512800.SS
* 515220.SS

## P2-B Negative Expectancy Detection

Completed

Watch List:

* 588000.SS
* 512660.SS
* 512800.SS

## P2-C Removal Simulation

Completed

Tested:

* Remove 588000.SS
* Remove 512660.SS
* Remove 512800.SS
* Remove 588000.SS + 512660.SS

Results:

588000.SS:

* Strong performance improvement after removal
* Sharpe increased significantly
* Excess return improved significantly
* Drawdown unchanged

512660.SS:

* Mild improvement when removed alone
* Combination test showed diversification value

512800.SS:

* Removal did not improve portfolio quality
* Slight deterioration in risk-adjusted returns

Decision:

Remove:

* 588000.SS

Retain:

* 512660.SS
* 512800.SS

P2 Closed.

# P3 - Ranking Engine Enhancement

Status: Pending

Goal:

Improve ranking quality.

Potential Work:

* Reduce Quality Score weight

* Reduce Liquidity Score weight

* Add trend persistence

* Add drawdown penalty

* Add slope stability factor

* Recalibrate ranking weights

## P3-A

增加：

Trend Persistence

回测

Status:

COMPLETED
KEEP = TRUE

## P3-B

如果有效：

增加：

Drawdown Penalty

再回测

P3-B Drawdown Penalty

Status:

COMPLETED

Result:

KEEP

## P3-C

如果有效：

增加：

Slope Stability

再回测

COMPLETED

Result:

KEEP

## MIG-007 Long-Term Robustness Validation

Status:
IN PROGRESS

TEST-001
2022 Bear Market Validation 2022-01-01~2022-12-31
Priority: CRITICAL
策略收益-12.02%，基准收益-21.63%，alpha-0.10,beta0.26,夏普-1.59，索提诺-2.31，最大回撤13.57%，策略年化收益率-12.39%，基准年化收益率-22.26%，超额收益8.90%，年化超额收益9.21%，日胜率52.48%，胜率23.81%，盈亏比52.39%，盈利次数20，亏损次数64，信息比率0.53，平均持仓时长17.04

TEST-002
2020 COVID Crash Validation 2020-01-01~2020-12-31
Priority: HIGH
策略收益15.47%，基准收益27.21%，alpha0.01,beta0.50,夏普0.93，索提诺1.21，最大回撤8.39%，策略年化收益率15.95%，基准年化收益率28.10%，超额收益-9.95%，年化超额收益-10.22%，日胜率50.21%，胜率50.62%，盈亏比140.79%，盈利次数41，亏损次数40，信息比率-0.81，平均持仓时长17.69

TEST-003
2021 Sector Rotation Validation 2021-01-01~2021-12-31
Priority: HIGH
策略收益2.11%，基准收益-5.20%，alpha0.02,beta0.40,夏普-0.17，索提诺-0.24，最大回撤8.79%，策略年化收益率2.17%，基准年化收益率-5.34%，超额收益8.00%，年化超额收益8.24%，日胜率50.21%，胜率42.17%，盈亏比88.51%，盈利次数35，亏损次数48，信息比率0.63，平均持仓时长16.88

TEST-004
2023 Sideways Market Validation 2023-01-01~2023-12-31
Priority: MEDIUM
策略收益-3.45%，基准收益-11.38%，alpha-0.02,beta0.34,夏普-0.96，索提诺-1.31，最大回撤8.47%，策略年化收益率-3.57%，基准年化收益率-11.73%，超额收益7.97%，年化超额收益8.24%，日胜率54.55%，胜率35.29%，盈亏比63.47%，盈利次数30，亏损次数55，信息比率0.76，平均持仓时长15.95

TEST-005
2020-2026 Full History Validation 2020-01-01~2026-06-24
Priority: FINAL
策略收益62.71%，基准收益20.66%，alpha0.05,beta0.43,夏普0.37，索提诺0.50，最大回撤20.25%，策略年化收益率8.08%，基准年化收益率3.04%，超额收益43.73%，年化超额收益5.96%，日胜率52.20%，胜率45.89%，盈亏比160.64%，盈利次数229，亏损次数270，信息比率0.40，平均持仓时长24.96

Status:
COMPLETED

Result:
PASS

Summary:

2020 COVID:
PARTIAL PASS

2021 Sector Rotation:
PASS

2022 Bear Market:
PASS+

2023 Sideways Market:
PASS+

2020-2026 Full Cycle:
PASS

Conclusion:

No obvious overfitting detected.

The P3 ranking enhancements
(Persistence + Drawdown + Stability)
show robust performance across multiple market regimes.

Strengths:

- Strong downside protection
- Positive long-term excess returns
- Low beta profile
- Consistent information ratio

Weaknesses:

- Conservative during strong bull markets
- Full-cycle Sharpe ratio remains relatively low
- Maximum drawdown still exceeds the medium-term target

Decision:

P3-A:
KEEP

P3-B:
STRONG KEEP

P3-C:
KEEP

---

## P3-D Weight Optimization

Version A（当前基线）：50/15/15/5/5/10
策略收益62.71%，基准收益20.66%，alpha0.05,beta0.43,夏普0.37，索提诺0.50，最大回撤20.25%，策略年化收益率8.08%，基准年化收益率3.04%，超额收益43.73%，年化超额收益5.96%，日胜率52.20%，胜率45.89%，盈亏比160.64%，盈利次数229，亏损次数270，信息比率0.40，平均持仓时长24.96

Version B（增强Drawdown）：45/15/15/10/5/10
策略收益52.77%，基准收益20.66%，alpha0.04,beta0.43,夏普0.27，索提诺0.37，最大回撤22.63%，策略年化收益率6.99%，基准年化收益率3.04%，超额收益33.80%，年化超额收益4.75%，日胜率52.27%，胜率45.74%，盈亏比151.97%，盈利次数231，亏损次数274，信息比率0.32，平均持仓时长24.54

Version C（增强Stability）：45/15/15/5/10/10
策略收益50.25%，基准收益20.66%，alpha0.03,beta0.43,夏普0.25，索提诺0.34，最大回撤22.03%，策略年化收益率6.71%，基准年化收益率3.04%，超额收益31.27%，年化超额收益4.44%，日胜率52.27%，胜率44.47%，盈亏比151.26%，盈利次数225，亏损次数281，信息比率0.30，平均持仓时长24.58

Version D（增强Liquidity）：45/15/15/5/5/15
策略收益57.88%，基准收益20.66%，alpha0.04,beta0.43,夏普0.32，索提诺0.44，最大回撤20.17%，策略年化收益率7.56%，基准年化收益率3.04%，超额收益38.90%，年化超额收益5.38%，日胜率52.58%，胜率46.23%，盈亏比161.13%，盈利次数227，亏损次数264，信息比率0.36，平均持仓时长25.51

Version E（恢复部分Momentum）：55/10/10/5/5/15
策略收益53.45%，基准收益20.66%，alpha0.04,beta0.43,夏普0.28，索提诺0.38，最大回撤21.92%，策略年化收益率7.07%，基准年化收益率3.04%，超额收益34.47%，年化超额收益4.84%，日胜率52.39%，胜率44.36%，盈亏比150.71%，盈利次数240，亏损次数301，信息比率0.33，平均持仓时长22.80

Status:
COMPLETED

Result:
NO CHANGE

Decision:

Keep:

50/15/15/5/5/10

as final production weights.

──────────────────

# P4 Bull Market Enhancement

Status: NEXT

Goal:

Improve participation during strong bull markets
while maintaining:

- Beta < 0.5
- MaxDD < 20%
- Positive long-term excess returns

Current weakness:

2020:

Strategy:
+15.47%

Benchmark:
+27.21%

Need:

Better upside participation without
destroying downside protection.

## P4-A Bull Regime Detection
回测区间	True	False	True占比	结论
2020	236	7	97.1%	通过
2022	2	240	0.8%	通过
2024~2025	311	174	64.1%	通过

目标：
验证 Bull Regime Detector 不影响现有策略逻辑。

检查：

- 收益率
- 夏普
- 最大回撤
- 调仓次数
- 持仓变化

完成标准：
与 P3 最终版本结果一致。

状态：
PASS

Status:
COMPLETED

## P4-B Dynamic Risk Exposure

### P4-B1 Dynamic Risk Target

目标：

Bull Market:

0.15 → 0.18

Bear/Normal:

保持0.15

完成标准：

代码实现完成。

2020(修改前)
策略收益15.47%，基准收益27.21%，alpha0.01,beta0.50,夏普0.93，索提诺1.21，最大回撤8.39%，策略年化收益率15.95%，基准年化收益率28.10%，超额收益-9.95%，年化超额收益-10.22%，日胜率50.21%，胜率50.62%，盈亏比140.79%，盈利次数41，亏损次数40，信息比率-0.81，平均持仓时长17.69

2020(修改后)
策略收益16.22%，基准收益27.21%，alpha0.01,beta0.54,夏普0.91，索提诺1.18，最大回撤10.07%，策略年化收益率16.72%，基准年化收益率28.10%，超额收益-9.20%，年化超额收益-9.45%，日胜率52.26%，胜率50.00%，盈亏比137.36%，盈利次数40，亏损次数40，信息比率-0.76，平均持仓时长17.94

2022(修改前)
策略收益-12.02%，基准收益-21.63%，alpha-0.10,beta0.26,夏普-1.59，索提诺-2.31，最大回撤13.57%，策略年化收益率-12.39%，基准年化收益率-22.26%，超额收益8.90%，年化超额收益9.21%，日胜率52.48%，胜率23.81%，盈亏比52.39%，盈利次数20，亏损次数64，信息比率0.53，平均持仓时长17.04

2022(修改后)
策略收益-13.00%，基准收益-21.63%，alpha-0.11,beta0.27,夏普-1.67，索提诺-2.46，最大回撤13.71%，策略年化收益率-13.40%，基准年化收益率-22.26%，超额收益7.93%，年化超额收益8.20%，日胜率52.48%，胜率23.81%，盈亏比59.20%，盈利次数20，亏损次数64，信息比率0.48，平均持仓时长17.08

2020-2026(修改前)
策略收益62.71%，基准收益20.66%，alpha0.05,beta0.43,夏普0.37，索提诺0.50，最大回撤20.25%，策略年化收益率8.08%，基准年化收益率3.04%，超额收益43.73%，年化超额收益5.96%，日胜率52.20%，胜率45.89%，盈亏比160.64%，盈利次数229，亏损次数270，信息比率0.40，平均持仓时长24.96

2020-2026(修改后)
策略收益60.28%，基准收益20.66%，alpha0.04,beta0.46,夏普0.32，索提诺0.44，最大回撤22.39%，策略年化收益率7.82%，基准年化收益率3.04%，超额收益41.30%，年化超额收益5.67%，日胜率52.71%，胜率45.71%，盈亏比155.06%，盈利次数229，亏损次数272，信息比率0.38，平均持仓时长24.68

状态：

FAILED

处理：

ROLLBACK

## P4-C Adaptive Cash Allocation

### P4-C1
Bull Allocation Audit

目标：

找出2020牛市真正的拖累资产。

完成后：

决定是否进入：

P4-C2
Bull Allocation Tilt

2020(修改前)
策略收益15.47%，基准收益27.21%，alpha0.01,beta0.50,夏普0.93，索提诺1.21，最大回撤8.39%，策略年化收益率15.95%，基准年化收益率28.10%，超额收益-9.95%，年化超额收益-10.22%，日胜率50.21%，胜率50.62%，盈亏比140.79%，盈利次数41，亏损次数40，信息比率-0.81，平均持仓时长17.69

2020(修改后)
策略收益26.87%，基准收益27.21%，alpha0.04,beta0.90,夏普1.03，索提诺1.37，最大回撤14.65%，策略年化收益率27.75%，基准年化收益率28.10%，超额收益1.46%，年化超额收益1.50%，日胜率47.74%，胜率48.81%，盈亏比129.08%，盈利次数41，亏损次数43，信息比率0.14，平均持仓时长17.12

2022(修改前)
策略收益-12.02%，基准收益-21.63%，alpha-0.10,beta0.26,夏普-1.59，索提诺-2.31，最大回撤13.57%，策略年化收益率-12.39%，基准年化收益率-22.26%，超额收益8.90%，年化超额收益9.21%，日胜率52.48%，胜率23.81%，盈亏比52.39%，盈利次数20，亏损次数64，信息比率0.53，平均持仓时长17.04

2022(修改后)
策略收益-10.73%，基准收益-21.63%，alpha-0.08,beta0.26,夏普-1.48，索提诺-2.24，最大回撤11.49%，策略年化收益率-11.06%，基准年化收益率-22.26%，超额收益10.19%，年化超额收益10.55%，日胜率52.07%，胜率23.17%，盈亏比49.58%，盈利次数19，亏损次数63，信息比率0.61，平均持仓时长13.17

2024.01.01-2025.12.31(修改前)
策略收益40.87%，基准收益34.94%，alpha0.09,beta0.47,夏普1.40，索提诺1.99，最大回撤9.08%，策略年化收益率19.32%，基准年化收益率16.70%，超额收益4.80%，年化超额收益2.45%，日胜率50.93%，胜率56.52%，盈亏比284.70%，盈利次数78，亏损次数60，信息比率0.18，平均持仓时长26.23

2024.01.01-2025.12.31(修改后)
策略收益38.79%，基准收益34.94%，alpha0.06,beta0.67,夏普0.91，索提诺1.23，最大回撤10.54%，策略年化收益率18.41%，基准年化收益率16.70%，超额收益2.73%，年化超额收益1.40%，日胜率53.81%，胜率54.61%，盈亏比195.32%，盈利次数77，亏损次数64，信息比率0.10，平均持仓时长23.60

#### P4-C1-001
Remove 518880

如果：

2024-2025:

+5%以上

同时：

2020下降<5%

2022恶化<3%

那么：

518880

Confirmed Alpha Drag

否则：

518880

Useful Diversifier

2020(全etf)
策略收益26.87%，基准收益27.21%，alpha0.04,beta0.90,夏普1.03，索提诺1.37，最大回撤14.65%，策略年化收益率27.75%，基准年化收益率28.10%，超额收益1.46%，年化超额收益1.50%，日胜率47.74%，胜率48.81%，盈亏比129.08%，盈利次数41，亏损次数43，信息比率0.14，平均持仓时长17.12
2020(no gold)
策略收益34.95%，基准收益27.21%，alpha0.10,beta1.02,夏普1.28，索提诺1.71，最大回撤15.35%，策略年化收益率36.12%，基准年化收益率28.10%，超额收益9.53%，年化超额收益9.82%，日胜率53.50%，胜率52.38%，盈亏比174.92%，盈利次数33，亏损次数30，信息比率0.96，平均持仓时长22.70

2022(全etf)
策略收益-10.73%，基准收益-21.63%，alpha-0.08,beta0.26,夏普-1.48，索提诺-2.24，最大回撤11.49%，策略年化收益率-11.06%，基准年化收益率-22.26%，超额收益10.19%，年化超额收益10.55%，日胜率52.07%，胜率23.17%，盈亏比49.58%，盈利次数19，亏损次数63，信息比率0.61，平均持仓时长13.17
2022(no gold)
策略收益-8.84%，基准收益-21.63%，alpha-0.04,beta0.37,夏普-0.96，索提诺-1.44，最大回撤14.89%，策略年化收益率-9.12%，基准年化收益率-22.26%，超额收益12.08%，年化超额收益12.50%，日胜率52.07%，胜率22.37%，盈亏比68.76%，盈利次数17，亏损次数59，信息比率0.72，平均持仓时长11.80

2024.01.01-2025.12.31(全etf)
策略收益38.79%，基准收益34.94%，alpha0.06,beta0.67,夏普0.91，索提诺1.23，最大回撤10.54%，策略年化收益率18.41%，基准年化收益率16.70%，超额收益2.73%，年化超额收益1.40%，日胜率53.81%，胜率54.61%，盈亏比195.32%，盈利次数77，亏损次数64，信息比率0.10，平均持仓时长23.60
2024.01.01-2025.12.31(no gold)
策略收益35.20%，基准收益34.94%，alpha0.01,beta0.88,夏普0.65，索提诺0.89，最大回撤15.92%，策略年化收益率16.82%，基准年化收益率16.70%，超额收益-0.86%，年化超额收益-0.44%，日胜率54.43%，胜率48.30%，盈亏比168.64%，盈利次数71，亏损次数76，信息比率-0.03，平均持仓时长21.27

Status:

COMPLETED

Conclusion:

518880 is NOT a confirmed alpha drag.

It improves: 2024-2025

and reduces: drawdowns.

#### P4-C1-002
Remove 510300

2020(全etf)
策略收益26.87%，基准收益27.21%，alpha0.04,beta0.90,夏普1.03，索提诺1.37，最大回撤14.65%，策略年化收益率27.75%，基准年化收益率28.10%，超额收益1.46%，年化超额收益1.50%，日胜率47.74%，胜率48.81%，盈亏比129.08%，盈利次数41，亏损次数43，信息比率0.14，平均持仓时长17.12
2020(Remove 510300)
策略收益25.53%，基准收益27.21%，alpha0.02,beta0.90,夏普0.96，索提诺1.29，最大回撤14.85%，策略年化收益率26.35%，基准年化收益率28.10%，超额收益0.11%，年化超额收益0.11%，日胜率47.74%，胜率51.28%，盈亏比137.54%，盈利次数40，亏损次数38，信息比率0.01，平均持仓时长19.38

2022(全etf)
策略收益-10.73%，基准收益-21.63%，alpha-0.08,beta0.26,夏普-1.48，索提诺-2.24，最大回撤11.49%，策略年化收益率-11.06%，基准年化收益率-22.26%，超额收益10.19%，年化超额收益10.55%，日胜率52.07%，胜率23.17%，盈亏比49.58%，盈利次数19，亏损次数63，信息比率0.61，平均持仓时长13.17
2022(Remove 510300)
策略收益-10.73%，基准收益-21.63%，alpha-0.08,beta0.26,夏普-1.48，索提诺-2.24，最大回撤11.49%，策略年化收益率-11.06%，基准年化收益率-22.26%，超额收益10.19%，年化超额收益10.55%，日胜率52.07%，胜率23.17%，盈亏比49.58%，盈利次数19，亏损次数63，信息比率0.61，平均持仓时长13.17

2024.01.01-2025.12.31(全etf)
策略收益38.79%，基准收益34.94%，alpha0.06,beta0.67,夏普0.91，索提诺1.23，最大回撤10.54%，策略年化收益率18.41%，基准年化收益率16.70%，超额收益2.73%，年化超额收益1.40%，日胜率53.81%，胜率54.61%，盈亏比195.32%，盈利次数77，亏损次数64，信息比率0.10，平均持仓时长23.60
2024.01.01-2025.12.31(Remove 510300)
策略收益45.67%，基准收益34.94%，alpha0.08,beta0.70,夏普1.05，索提诺1.43，最大回撤10.22%，策略年化收益率21.40%，基准年化收益率16.70%，超额收益9.61%，年化超额收益4.84%，日胜率54.64%，胜率55.37%，盈亏比209.14%，盈利次数67，亏损次数54，信息比率0.35，平均持仓时长27.52

Status:

Completed

Conclusion:

510300 is a confirmed bull-market alpha drag.

#### P4-C1-003
Remove 510500

2020(全etf)
策略收益26.87%，基准收益27.21%，alpha0.04,beta0.90,夏普1.03，索提诺1.37，最大回撤14.65%，策略年化收益率27.75%，基准年化收益率28.10%，超额收益1.46%，年化超额收益1.50%，日胜率47.74%，胜率48.81%，盈亏比129.08%，盈利次数41，亏损次数43，信息比率0.14，平均持仓时长17.12
2020(Remove 510500)
策略收益32.36%，基准收益27.21%，alpha0.09,beta0.91,夏普1.27，索提诺1.71，最大回撤14.62%，策略年化收益率33.43%，基准年化收益率28.10%，超额收益6.94%，年化超额收益7.15%，日胜率49.38%，胜率43.33%，盈亏比158.10%，盈利次数26，亏损次数34，信息比率0.65，平均持仓时长23.22

2022(全etf)
策略收益-10.73%，基准收益-21.63%，alpha-0.08,beta0.26,夏普-1.48，索提诺-2.24，最大回撤11.49%，策略年化收益率-11.06%，基准年化收益率-22.26%，超额收益10.19%，年化超额收益10.55%，日胜率52.07%，胜率23.17%，盈亏比49.58%，盈利次数19，亏损次数63，信息比率0.61，平均持仓时长13.17
2022(Remove 510500)
策略收益-11.28%，基准收益-21.63%，alpha-0.09,beta0.26,夏普-1.52，索提诺-2.33，最大回撤11.76%，策略年化收益率-11.64%，基准年化收益率-22.26%，超额收益9.64%，年化超额收益9.97%，日胜率51.24%，胜率25.00%，盈亏比48.97%，盈利次数21，亏损次数63，信息比率0.57，平均持仓时长12.64

2024.01.01-2025.12.31(全etf)
策略收益38.79%，基准收益34.94%，alpha0.06,beta0.67,夏普0.91，索提诺1.23，最大回撤10.54%，策略年化收益率18.41%，基准年化收益率16.70%，超额收益2.73%，年化超额收益1.40%，日胜率53.81%，胜率54.61%，盈亏比195.32%，盈利次数77，亏损次数64，信息比率0.10，平均持仓时长23.60
2024.01.01-2025.12.31(Remove 510500)
策略收益38.38%，基准收益34.94%，alpha0.05,beta0.66,夏普0.90，索提诺1.22，最大回撤10.54%，策略年化收益率18.23%，基准年化收益率16.70%，超额收益2.32%，年化超额收益1.19%，日胜率54.23%，胜率48.36%，盈亏比197.64%，盈利次数59，亏损次数63，信息比率0.09，平均持仓时长27.23

Status:

COMPLETE

Conclusion:

Neutral Asset

### P4-C1-004
Tech Only Portfolio

2020(全etf)
策略收益26.87%，基准收益27.21%，alpha0.04,beta0.90,夏普1.03，索提诺1.37，最大回撤14.65%，策略年化收益率27.75%，基准年化收益率28.10%，超额收益1.46%，年化超额收益1.50%，日胜率47.74%，胜率48.81%，盈亏比129.08%，盈利次数41，亏损次数43，信息比率0.14，平均持仓时长17.12
2020(Tech Only)
策略收益-5.23%，基准收益27.21%，alpha-0.34,beta1.11,夏普-0.30，索提诺-0.41，最大回撤24.01%，策略年化收益率-5.38%，基准年化收益率28.10%，超额收益-30.65%，年化超额收益-31.37%，日胜率43.62%，胜率16.67%，盈亏比67.46%，盈利次数2，亏损次数10，信息比率-1.68，平均持仓时长42.42

2022(全etf)
策略收益-10.73%，基准收益-21.63%，alpha-0.08,beta0.26,夏普-1.48，索提诺-2.24，最大回撤11.49%，策略年化收益率-11.06%，基准年化收益率-22.26%，超额收益10.19%，年化超额收益10.55%，日胜率52.07%，胜率23.17%，盈亏比49.58%，盈利次数19，亏损次数63，信息比率0.61，平均持仓时长13.17
2022(Tech Only)
策略收益-8.81%，基准收益-21.63%，alpha-0.12,beta0.04,夏普-2.59，索提诺-4.38，最大回撤9.39%，策略年化收益率-9.09%，基准年化收益率-22.26%，超额收益12.11%，年化超额收益12.54%，日胜率52.07%，胜率37.50%，盈亏比9.46%，盈利次数3，亏损次数5，信息比率0.63，平均持仓时长9.00

2024.01.01-2025.12.31(全etf)
策略收益38.79%，基准收益34.94%，alpha0.06,beta0.67,夏普0.91，索提诺1.23，最大回撤10.54%，策略年化收益率18.41%，基准年化收益率16.70%，超额收益2.73%，年化超额收益1.40%，日胜率53.81%，胜率54.61%，盈亏比195.32%，盈利次数77，亏损次数64，信息比率0.10，平均持仓时长23.60
2024.01.01-2025.12.31(Tech Only)
策略收益31.78%，基准收益34.94%，alpha0.01,beta0.81,夏普0.49，索提诺0.72，最大回撤20.30%，策略年化收益率15.29%，基准年化收益率16.70%，超额收益-4.28%，年化超额收益-2.23%，日胜率52.99%，胜率33.33%，盈亏比33.28%，盈利次数7，亏损次数14，信息比率-0.11，平均持仓时长51.81

STATUS:

COMPLETE

最终结论：

Asset	Final Verdict
518880	Regime-Dependent Diversifier
510300	Confirmed Bull Alpha Drag
510500	Neutral Diversifier
TECH_ONLY	Invalid Portfolio Construction

### P4-C2 Bull Large-Cap De-emphasis

### P4-C2-001 Allocation Audit
COMPLETED

Findings:

Broad ETF concentration is common:

broad=0:
24%

broad=1:
33%

broad=2:
27%

broad=3:
15%

510300 appears to compete primarily
for the final portfolio slot rather
than dominating allocations.

### P4-C2-002 Soft Penalty Test

Bull Market: 510300 score *= 0.90

2020(修改前)
策略收益26.87%，基准收益27.21%，alpha0.04,beta0.90,夏普1.03，索提诺1.37，最大回撤14.65%，策略年化收益率27.75%，基准年化收益率28.10%，超额收益1.46%，年化超额收益1.50%，日胜率47.74%，胜率48.81%，盈亏比129.08%，盈利次数41，亏损次数43，信息比率0.14，平均持仓时长17.12
2020(Soft Penalty)
策略收益28.55%，基准收益27.21%，alpha0.05,beta0.90,夏普1.11，索提诺1.47，最大回撤14.87%，策略年化收益率29.48%，基准年化收益率28.10%，超额收益3.13%，年化超额收益3.22%，日胜率48.15%，胜率47.95%，盈亏比139.54%，盈利次数35，亏损次数38，信息比率0.29，平均持仓时长19.90

2024.01.01-2025.12.31(修改前)
策略收益38.79%，基准收益34.94%，alpha0.06,beta0.67,夏普0.91，索提诺1.23，最大回撤10.54%，策略年化收益率18.41%，基准年化收益率16.70%，超额收益2.73%，年化超额收益1.40%，日胜率53.81%，胜率54.61%，盈亏比195.32%，盈利次数77，亏损次数64，信息比率0.10，平均持仓时长23.60
2024.01.01-2025.12.31(Soft Penalty)
策略收益41.74%，基准收益34.94%，alpha0.07,beta0.67,夏普0.97，索提诺1.32，最大回撤11.08%，策略年化收益率19.70%，基准年化收益率16.70%，超额收益5.68%，年化超额收益2.89%，日胜率54.43%，胜率54.35%，盈亏比191.22%，盈利次数75，亏损次数63，信息比率0.21，平均持仓时长21.43

2020-2026(修改前)
策略收益62.71%，基准收益20.66%，alpha0.05,beta0.43,夏普0.37，索提诺0.50，最大回撤20.25%，策略年化收益率8.08%，基准年化收益率3.04%，超额收益43.73%，年化超额收益5.96%，日胜率52.20%，胜率45.89%，盈亏比160.64%，盈利次数229，亏损次数270，信息比率0.40，平均持仓时长24.96
2020-2026(Soft Penalty)
策略收益99.74%，基准收益20.66%，alpha0.08,beta0.68,夏普0.43，索提诺0.58，最大回撤23.48%，策略年化收益率11.67%，基准年化收益率3.04%，超额收益80.77%，年化超额收益9.91%，日胜率53.10%，胜率43.71%，盈亏比156.31%，盈利次数212，亏损次数273，信息比率0.63，平均持仓时长23.53

STATUS:

COMPLETED

Replaced hard broad-category exclusion with a
soft diversification penalty.

Final Design:

broad_count = 0:

factor = 1.00

broad_count = 1:

factor = 0.95

broad_count = 2:

factor = 0.90

broad_count >= 3:

factor = 0.85

Validation:

2020:

Improved returns and Sharpe ratio.

2024-2025:

Improved participation in multi-theme bull markets.

2020-2026:

Total return:

62.71% -> 99.74%

Annualized:

8.08% -> 11.67%

Information Ratio:

0.40 -> 0.63

Maximum Drawdown:

20.25% -> 23.48%

---

## P4-D Forward Stability Validation

STATUS:

IN PROGRESS

Goal:

Validate the robustness of P4 bull-market
enhancements under recent market conditions.

Validation Window:

2026-04-01 ~ 2026-06-24

Focus:

- Position stability
- Turnover behavior
- Broad ETF allocation patterns
- Sector rotation consistency
- Risk control behavior

No further parameter tuning allowed unless
critical defects are discovered.