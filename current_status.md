# current phase:
    P1

# current focus:
    分析P1的问题，拆分成小任务逐个解决

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

