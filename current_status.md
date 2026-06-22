# current phase:
    P0

# current focus:
    EXEC-005 Threshold Bug Fix

Latest Result:
发现执行层Bug：

order_target_percent()
中的threshold变量在卖单路径未定义。

导致：

- SELL_REMOVED全部失败
- 仓位未更新
- 后续BUY资金不足

Next Action:
修复threshold逻辑后重新回测。

# task_list:

## P0

EXEC-001 Cash Check
Status: Completed

EXEC-002 Commission Buffer
Status: Completed

EXEC-003 Sell First
Status: Completed

实现：

- 卖单优先执行
- 买单后执行

验证：

- 长周期回测通过
- 无资金不足
- 无现金不足

结论：

无需升级为T+1调仓

EXEC-004 Scaled Buy (Optional)
Status: Cancelled
Reason:

EXEC-001~003 已解决执行层问题。
回测未再出现资金不足、现金不足或0股委托。
分批买入不再具备明确收益。

EXEC-005 Threshold Bug Fix
Status: Pending

1. threshold bug修复

2. 短回测
2026-05-25 ~ 2026-06-30

验证：
- REMOVE仓位消失
- CURRENT变化
- TARGET达成
- 无资金不足异常

3. 长回测
2024-01-01 ~ 2025-12-31

验证：
- 调仓正常
- 现金ETF正常
- 无执行层异常