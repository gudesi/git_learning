"""
PTrade 量化策略 —— 多因子 ETF 轮动（最终版）

特点：
- 配置集中管理，便于调整参数
- 预计算宇宙一次性拉取所有指标与横截面排序，杜绝重复计算
- 指标函数底层缓存，跨资产共享
- 排名、权重、风险控制链路无冗余计算
- 再平衡流程清晰：清仓 → 调仓
"""

import math
import bisect
from functools import wraps
from typing import List, Dict, Optional, Tuple, Any


# =========================================================
# 全局配置
# =========================================================
class Config:
    # 现金等价物
    CASH_ETF = "511880.SS"

    # 资产池                   
    BROAD_ETFS    = ["510300.SS", "510500.SS", "512100.SS", "563300.SS",
                     "159915.SZ",  "510880.SS"]                       
    FINANCIAL_ETFS = ["512880.SS", "512800.SS"]
    TECH_ETFS      = ["512480.SS", "159819.SZ", "562500.SS", "512980.SS", "516160.SS"]
    DEFENSE_ETFS   = ["512660.SS"]
    HEALTHCARE_ETFS = ["512010.SS"]
    CONSUMER_ETFS  = ["159928.SZ"]
    RESOURCE_ETFS  = ["512400.SS", "518880.SS", "515220.SS"]
    RISK_ETFS = tuple(BROAD_ETFS + FINANCIAL_ETFS + TECH_ETFS +
                      DEFENSE_ETFS + HEALTHCARE_ETFS + CONSUMER_ETFS + RESOURCE_ETFS)

    # 精度与阈值
    EPSILON = 1e-8
    MIN_CASH_WEIGHT = 1e-4
    CASH_MIN_TRADE_PCT = 0.005
    CASH_MIN_TRADE_ABS = 12000
    STOCK_MIN_TRADE_ABS = 1000

    # 指标参数
    RETURN_WINDOWS = (20, 60, 120, 250)
    ATR_LOOKBACK = 20
    LIQUIDITY_LOOKBACK = 60
    QUALITY_LOOKBACK = 120

    PERSISTENCE_LOOKBACK = 120
    PERSISTENCE_MA_WINDOW = 20

    DRAWDOWN_LOOKBACK = 120
    STABILITY_LOOKBACK = 120

    MOMENTUM_WEIGHTS = {20: 0.05, 60: 0.15, 120: 0.30, 250: 0.50}
    MOMENTUM_SCORE_WEIGHT = 0.50
    QUALITY_SCORE_WEIGHT = 0.15
    PERSISTENCE_SCORE_WEIGHT = 0.15
    DRAWDOWN_SCORE_WEIGHT = 0.05
    STABILITY_SCORE_WEIGHT = 0.05
    LIQUIDITY_SCORE_WEIGHT = 0.10

    # 组合构建
    MAX_PORTFOLIO_SIZE = 5
    RANKING_TREND_MA = 200
    TARGET_PORTFOLIO_RISK = 0.15
    MAX_SINGLE_POSITION_WEIGHT = 0.25
    MIN_SINGLE_POSITION_WEIGHT = 0.05

    # 风险控制
    LOW_RISK_THRESHOLD = 0.80
    HIGH_RISK_THRESHOLD = 1.00
    EXTREME_RISK_THRESHOLD = 1.20
    LOW_RISK_EXPOSURE = 1.00
    HIGH_RISK_EXPOSURE = 0.90
    EXTREME_RISK_EXPOSURE = 0.75
    DEFENSIVE_EXPOSURE = 0.50

    # 交易执行
    REBALANCE_TOLERANCE = 0.01
    COMMISSION_BUFFER = 0.98
    MAX_WEIGHT_ITER = 10


# =========================================================
# 工具函数
# =========================================================
def normalize_symbol(symbol: str) -> str:
    """统一 XSHG/XSHE → SS/SZ"""
    if symbol.endswith(".XSHG"):
        return symbol.replace(".XSHG", ".SS")
    if symbol.endswith(".XSHE"):
        return symbol.replace(".XSHE", ".SZ")
    return symbol


# =========================================================
# 轻量缓存管理
# =========================================================
GLOBAL_CACHE = {}

def clear_cache():
    GLOBAL_CACHE.clear()

def cached(prefix: str):
    """仅接受可哈希参数，避免字典作为键"""
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (prefix,) + args if args else prefix
            if key in GLOBAL_CACHE:
                return GLOBAL_CACHE[key]
            result = func(*args, **kwargs)
            GLOBAL_CACHE[key] = result
            return result
        return wrapper
    return deco


# =========================================================
# 底层历史数据 (带缓存)
# =========================================================
@cached("history")
def _get_history_field(symbol: str, field: str, count: int) -> List[float]:
    try:
        data = get_history(count, '1d', field, symbol, fq='post', include=False)
        if data is None:
            return []
        if hasattr(data, "values") and hasattr(data, "columns"):
            if field in data.columns:
                return list(data[field].values)
            if len(data.columns) == 1:
                return list(data.iloc[:, 0].values)
        if hasattr(data, "tolist"):
            return data.tolist()
        return list(data)
    except Exception as e:
        log.error(f"HISTORY_FAILED {symbol} {field} {count}: {e}")
        return []

def get_close(symbol: str, count: int) -> List[float]:
    return _get_history_field(symbol, 'close', count)

def get_high(symbol: str, count: int) -> List[float]:
    return _get_history_field(symbol, 'high', count)

def get_low(symbol: str, count: int) -> List[float]:
    return _get_history_field(symbol, 'low', count)

def get_turnover(symbol: str, count: int) -> List[float]:
    return _get_history_field(symbol, 'money', count)


# =========================================================
# 原始指标计算 (底层均缓存)
# =========================================================
@cached("return")
def calc_return(symbol: str, lookback: int) -> Optional[float]:
    if lookback not in Config.RETURN_WINDOWS:
        raise ValueError(f"Unsupported lookback: {lookback}")
    close = get_close(symbol, lookback + 1)
    if len(close) < lookback + 1 or close[0] <= 0:
        return None
    return close[-1] / close[0] - 1.0

@cached("volatility")
def calc_volatility(symbol: str, lookback: int = 60) -> Optional[float]:
    close = get_close(symbol, lookback + 1)
    if len(close) < lookback + 1:
        return None
    returns = [close[i] / close[i-1] - 1 for i in range(1, len(close))]
    n = len(returns)
    if n < 2:
        return None
    mean = sum(returns) / n
    variance = sum((r - mean) ** 2 for r in returns) / (n - 1)
    return math.sqrt(variance * 252)

@cached("risk_adj_momentum")
def calc_risk_adjusted_momentum(symbol: str, lookback: int) -> Optional[float]:
    ret = calc_return(symbol, lookback)
    vol = calc_volatility(symbol, 60)
    if ret is None or vol is None or vol <= 0:
        return None
    return ret / vol

@cached("trend_quality")
def calc_trend_quality_raw(symbol: str, lookback: int = Config.QUALITY_LOOKBACK) -> Optional[float]:
    close = get_close(symbol, lookback)
    if len(close) < lookback or min(close) <= 0:
        return None
    log_prices = [math.log(p) for p in close]
    n = len(log_prices)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(log_prices) / n
    num = sum((x[i] - x_mean) * (log_prices[i] - y_mean) for i in range(n))
    den = sum((x[i] - x_mean) ** 2 for i in range(n))
    if den == 0:
        return None
    slope = num / den
    ss_total = sum((y - y_mean) ** 2 for y in log_prices)
    if ss_total <= 0:
        return None
    ss_res = sum((log_prices[i] - (y_mean + slope * (x[i] - x_mean))) ** 2 for i in range(n))
    r_sq = 1.0 - ss_res / ss_total
    return slope * r_sq

@cached("trend_persistence")
def calc_trend_persistence_raw(
    symbol: str,
    lookback: int = Config.PERSISTENCE_LOOKBACK,
    ma_window: int = Config.PERSISTENCE_MA_WINDOW
) -> Optional[float]:

    close = get_close(symbol, lookback + ma_window)

    if len(close) < lookback + ma_window:
        return None

    days_above_ma = 0

    for i in range(ma_window, len(close)):

        ma = sum(close[i - ma_window:i]) / ma_window

        if close[i] > ma:
            days_above_ma += 1

    return days_above_ma / float(lookback)

@cached("max_drawdown")
def calc_max_drawdown_raw(
    symbol: str,
    lookback: int = Config.DRAWDOWN_LOOKBACK
) -> Optional[float]:

    close = get_close(symbol, lookback)

    if len(close) < lookback:
        return None

    peak = close[0]
    max_dd = 0.0

    for price in close:

        if price > peak:
            peak = price

        if peak > 0:

            drawdown = (peak - price) / peak

            if drawdown > max_dd:
                max_dd = drawdown

    # 转成分数
    # 回撤越小越接近1
    return 1.0 - max_dd

@cached("trend_stability")
def calc_trend_stability_raw(
    symbol: str,
    lookback: int = Config.STABILITY_LOOKBACK
) -> Optional[float]:

    close = get_close(symbol, lookback + 1)

    if len(close) < lookback + 1:
        return None

    returns = []

    for i in range(1, len(close)):

        if close[i - 1] <= 0:
            return None

        returns.append(
            close[i] / close[i - 1] - 1
        )

    if len(returns) < 2:
        return None

    mean_ret = sum(returns) / len(returns)

    variance = sum(
        (r - mean_ret) ** 2
        for r in returns
    ) / (len(returns) - 1)

    std = math.sqrt(variance)

    if std <= 0:
        return None

    return 1.0 / std

@cached("adv")
def calc_adv60(symbol: str, lookback: int = Config.LIQUIDITY_LOOKBACK) -> Optional[float]:
    turnover = get_turnover(symbol, lookback)
    if not turnover or len(turnover) < lookback:
        return None
    return sum(turnover) / len(turnover)

@cached("atr")
def calc_atr(symbol: str, lookback: int = Config.ATR_LOOKBACK) -> Optional[float]:
    high = get_high(symbol, lookback + 1)
    low = get_low(symbol, lookback + 1)
    close = get_close(symbol, lookback + 1)
    if len(high) < lookback + 1 or len(low) < lookback + 1 or len(close) < lookback + 1:
        return None
    tr = [max(high[i] - low[i], abs(high[i] - close[i-1]), abs(low[i] - close[i-1]))
          for i in range(1, len(close))]
    return sum(tr) / len(tr) if tr else None

def calc_atr_percent(symbol: str) -> Optional[float]:
    atr = calc_atr(symbol)
    close = get_close(symbol, 1)
    if atr is None or not close or close[-1] <= 0:
        return None
    return atr / close[-1]

# =========================================================
# 宇宙预计算 + 横截面排序 (一次性构建，杜绝重复)
# =========================================================
def precompute_universe() -> Dict[str, Any]:
    cache_key = "precomputed_universe"
    if cache_key in GLOBAL_CACHE:
        return GLOBAL_CACHE[cache_key]

    # 收集所有原始指标
    risk_adj_mom = {}
    trend_q_raw = {}
    trend_persistence_raw = {}
    drawdown_raw = {}
    stability_raw = {}
    adv60_dict = {}

    for sym in Config.RISK_ETFS:
        mom_dict = {}
        for lb in Config.RETURN_WINDOWS:
            val = calc_risk_adjusted_momentum(sym, lb)
            if val is not None:
                mom_dict[lb] = val
        risk_adj_mom[sym] = mom_dict

        q = calc_trend_quality_raw(sym)
        if q is not None:
            trend_q_raw[sym] = q

        p = calc_trend_persistence_raw(sym)
        if p is not None:
            trend_persistence_raw[sym] = p

        dd = calc_max_drawdown_raw(sym)
        if dd is not None:
            drawdown_raw[sym] = dd

        st = calc_trend_stability_raw(sym)
        if st is not None:
            stability_raw[sym] = st

        adv = calc_adv60(sym)
        if adv is not None:
            adv60_dict[sym] = adv

    # 一次性构建所有横截面排序列表
    momentum_cross = {
        lb: sorted([v[lb] for v in risk_adj_mom.values() if lb in v])
        for lb in Config.RETURN_WINDOWS
    }
    quality_cross = sorted(
        [v for v in trend_q_raw.values() if v is not None]
    )

    persistence_cross = sorted(
        [v for v in trend_persistence_raw.values() if v is not None]
    )

    drawdown_cross = sorted(
        [v for v in drawdown_raw.values() if v is not None]
    )

    stability_cross = sorted(
        v for v in stability_raw.values()
        if v is not None
    )

    liquidity_cross = sorted(
        [v for v in adv60_dict.values() if v is not None]
    )

    universe = {
        "risk_adj_momentum": risk_adj_mom,
        "trend_quality_raw": trend_q_raw,
        "trend_persistence_raw": trend_persistence_raw,
        "drawdown_raw": drawdown_raw,
        "stability_raw": stability_raw,
        "adv60": adv60_dict,

        "momentum_cross_sections": momentum_cross,
        "quality_cross_section": quality_cross,
        "persistence_cross_section": persistence_cross,
        "drawdown_cross_section": drawdown_cross,
        "stability_cross_section": stability_cross,
        "liquidity_cross_section": liquidity_cross,
    }
    GLOBAL_CACHE[cache_key] = universe
    return universe


def _percentile_rank(value: float, sorted_list: List[float]) -> float:
    if len(sorted_list) <= 1:
        return 0.5
    rank = bisect.bisect_right(sorted_list, value)
    return (rank - 1) / (len(sorted_list) - 1)


# =========================================================
# 得分计算 (纯读取预计算数据)
# =========================================================
def calc_momentum_score(symbol: str, universe: Dict[str, Any]) -> Optional[float]:
    data = universe["risk_adj_momentum"].get(symbol)
    if not data:
        return None
    total = 0.0
    for lb in Config.RETURN_WINDOWS:
        raw = data.get(lb)
        cross = universe["momentum_cross_sections"].get(lb)
        if raw is None or cross is None:
            return None
        total += Config.MOMENTUM_WEIGHTS[lb] * _percentile_rank(raw, cross)
    return total

def calc_quality_score(symbol: str, universe: Dict[str, Any]) -> Optional[float]:
    raw = universe["trend_quality_raw"].get(symbol)
    cross = universe.get("quality_cross_section")
    if raw is None or not cross:
        return None
    return _percentile_rank(raw, cross)

def calc_persistence_score(
    symbol: str,
    universe: Dict[str, Any]
) -> Optional[float]:

    raw = universe["trend_persistence_raw"].get(symbol)

    cross = universe.get("persistence_cross_section")

    if raw is None or not cross:
        return None

    return _percentile_rank(raw, cross)

def calc_drawdown_score(
    symbol: str,
    universe: Dict[str, Any]
) -> Optional[float]:

    raw = universe["drawdown_raw"].get(symbol)

    cross = universe.get("drawdown_cross_section")

    if raw is None or not cross:
        return None

    return _percentile_rank(raw, cross)

def calc_stability_score(
    symbol: str,
    universe: Dict[str, Any]
) -> Optional[float]:

    raw = universe["stability_raw"].get(symbol)

    cross = universe.get(
        "stability_cross_section"
    )

    if raw is None or not cross:
        return None

    return _percentile_rank(raw, cross)

def calc_liquidity_score(symbol: str, universe: Dict[str, Any]) -> Optional[float]:
    raw = universe["adv60"].get(symbol)
    cross = universe.get("liquidity_cross_section")
    if raw is None or not cross:
        return None
    return _percentile_rank(raw, cross)

def calc_final_score(
    symbol,
    universe
):

    m = calc_momentum_score(symbol, universe)

    q = calc_quality_score(symbol, universe)

    p = calc_persistence_score(symbol, universe)

    d = calc_drawdown_score(symbol, universe)

    s = calc_stability_score(symbol, universe)

    l = calc_liquidity_score(symbol, universe)

    if None in (m, q, p, d, s, l):
        return None

    return (

        Config.MOMENTUM_SCORE_WEIGHT * m +

        Config.QUALITY_SCORE_WEIGHT * q +

        Config.PERSISTENCE_SCORE_WEIGHT * p +

        Config.DRAWDOWN_SCORE_WEIGHT * d +

        Config.STABILITY_SCORE_WEIGHT * s +

        Config.LIQUIDITY_SCORE_WEIGHT * l

    )

# =========================================================
# 排名与选股
# =========================================================
def build_ranking_table(
    universe: Dict[str, Any]
) -> List[Tuple[str, float]]:

    scored = []

    for sym in Config.RISK_ETFS:

        m = calc_momentum_score(sym, universe)
        q = calc_quality_score(sym, universe)
        p = calc_persistence_score(sym, universe)
        d = calc_drawdown_score(sym, universe)
        l = calc_liquidity_score(sym, universe)

        final = calc_final_score(sym, universe)

        if final is None:
            continue

        log.info(
            f"RANK {sym} "
            f"M={m:.3f} "
            f"Q={q:.3f} "
            f"P={p:.3f} "
            f"D={d:.3f} "
            f"L={l:.3f} "
            f"F={final:.3f}"
        )

        scored.append((sym, final))

    scored.sort(key=lambda x: x[1], reverse=True)

    return scored

def passes_ranking_filter(symbol: str) -> bool:
    close = get_close(symbol, Config.RANKING_TREND_MA)
    if len(close) < Config.RANKING_TREND_MA:
        return False
    return close[-1] > (sum(close) / Config.RANKING_TREND_MA)

def get_selected_etfs(universe: Dict[str, Any]) -> List[str]:
    candidates = [(s, sc) for s, sc in build_ranking_table(universe) if passes_ranking_filter(s)]
    return [s for s, _ in candidates[:Config.MAX_PORTFOLIO_SIZE]]


# =========================================================
# 权重生成与约束
# =========================================================
def calc_inverse_volatility_weights(symbols: List[str]) -> Dict[str, float]:
    risk_vals = {}
    for s in symbols:
        atr_pct = calc_atr_percent(s)
        if atr_pct and atr_pct > 0:
            risk_vals[s] = 1.0 / atr_pct
    if not risk_vals:
        return {}
    total = sum(risk_vals.values())
    return {s: v / total for s, v in risk_vals.items()}

def calc_initial_weights(universe: Dict[str, Any]) -> Dict[str, float]:
    selected = get_selected_etfs(universe)
    return calc_inverse_volatility_weights(selected)

def normalize_weights(w: Dict[str, float]) -> Dict[str, float]:
    t = sum(w.values())
    return {s: v / t for s, v in w.items()} if t > 0 else {}

def apply_max_position_constraint(w: Dict[str, float]) -> Dict[str, float]:
    adj = w.copy()
    for _ in range(20):
        excess = sum(max(0, adj[s] - Config.MAX_SINGLE_POSITION_WEIGHT) for s in adj)
        for s in adj:
            if adj[s] > Config.MAX_SINGLE_POSITION_WEIGHT:
                adj[s] = Config.MAX_SINGLE_POSITION_WEIGHT
        if excess <= Config.EPSILON:
            break
        eligible = [s for s, wt in adj.items() if wt < Config.MAX_SINGLE_POSITION_WEIGHT]
        if not eligible:
            break
        total_el = sum(adj[s] for s in eligible)
        for s in eligible:
            adj[s] += excess * (adj[s] / total_el) if total_el > 0 else excess / len(eligible)
    return adj

def apply_min_position_constraint(w: Dict[str, float]) -> Dict[str, float]:
    return {s: wt for s, wt in w.items() if wt >= Config.MIN_SINGLE_POSITION_WEIGHT}

def apply_position_constraints(w: Dict[str, float]) -> Dict[str, float]:
    if not w:
        return {}
    adj = w.copy()
    for _ in range(Config.MAX_WEIGHT_ITER):
        prev = adj.copy()
        adj = apply_max_position_constraint(adj)
        adj = normalize_weights(adj)
        adj = apply_min_position_constraint(adj)
        adj = normalize_weights(adj)
        if all(abs(adj.get(s, 0) - prev.get(s, 0)) < Config.EPSILON for s in set(adj) | set(prev)):
            break
    return adj

def get_target_weights(universe: Dict[str, Any]) -> Dict[str, float]:
    return apply_position_constraints(calc_initial_weights(universe))


# =========================================================
# 风险度量与调整
# =========================================================
def calc_portfolio_atr(weights: Dict[str, float]) -> Optional[float]:
    total_risk, total_w = 0.0, 0.0
    for s, w in weights.items():
        atr_pct = calc_atr_percent(s)
        if atr_pct is not None:
            total_risk += atr_pct * w
            total_w += w
    return total_risk / total_w if total_w > 0 else None

def calc_weighted_average_volatility(weights: Dict[str, float]) -> Optional[float]:
    total_vol, total_w = 0.0, 0.0
    for s, w in weights.items():
        vol = calc_volatility(s)
        if vol is not None:
            total_vol += vol * w
            total_w += w
    return total_vol / total_w if total_w > 0 else None

def calc_risk_budget_usage(weights: Dict[str, float]) -> Optional[float]:
    pvol = calc_weighted_average_volatility(weights)
    if pvol is None or Config.TARGET_PORTFOLIO_RISK <= 0:
        return None
    return pvol / Config.TARGET_PORTFOLIO_RISK

def get_risk_scaling_factor(weights: Dict[str, float]) -> float:
    usage = calc_risk_budget_usage(weights)
    if usage is None:
        return 1.0
    if usage < Config.LOW_RISK_THRESHOLD:
        return Config.LOW_RISK_EXPOSURE
    if usage < Config.HIGH_RISK_THRESHOLD:
        return Config.HIGH_RISK_EXPOSURE
    if usage < Config.EXTREME_RISK_THRESHOLD:
        return Config.EXTREME_RISK_EXPOSURE
    return Config.DEFENSIVE_EXPOSURE

def calc_market_exposure() -> float:
    return 1.0

def get_risk_adjusted_weights(target_weights: Dict[str, float], risk_factor: float) -> Dict[str, float]:
    if not target_weights:
        return {}
    factor = risk_factor * calc_market_exposure()
    return {s: w * factor for s, w in target_weights.items()}

def get_cash_weight(weights: Dict[str, float]) -> float:
    invested = sum(weights.values())
    cash = max(0.0, 1.0 - invested)
    return cash if cash >= Config.MIN_CASH_WEIGHT else 0.0


# =========================================================
# 订单执行
# =========================================================
def get_normalized_positions_live() -> Dict[str, Any]:
    pos = get_positions()
    return {normalize_symbol(s): p for s, p in pos.items()} if pos else {}

def get_position_value(symbol: str) -> float:
    p = get_normalized_positions_live().get(symbol)
    if p is None:
        return 0.0
    try:
        return float(p.amount) * float(p.last_sale_price)
    except Exception:
        return 0.0

def order_target_percent(context, symbol: str, target_pct: float):
    try:
        total_eq = float(context.portfolio.portfolio_value)
        target_val = total_eq * target_pct * Config.COMMISSION_BUFFER
        delta = target_val - get_position_value(symbol)
        if delta > 0:
            if symbol == Config.CASH_ETF:
                threshold = max(total_eq * Config.CASH_MIN_TRADE_PCT, Config.CASH_MIN_TRADE_ABS)
            else:
                threshold = Config.STOCK_MIN_TRADE_ABS
            if delta < threshold:
                log.info(f"ORDER_SKIPPED {symbol} delta={delta:.2f} < threshold={threshold:.2f}")
                return None
        return order_value(symbol, delta)
    except Exception as e:
        log.info(f"ORDER_TARGET_EXCEPTION {symbol}: {e}")
        return None


# =========================================================
# 再平衡引擎
# =========================================================
def rebalance(context, risk_weights: Dict[str, float], cash_weight: float):
    """传入已计算的权重，内部不再重复计算"""
    all_targets = dict(risk_weights)
    if cash_weight > 0:
        all_targets[Config.CASH_ETF] = cash_weight

    target_symbols = set(all_targets.keys())
    current_pos = get_positions()
    current_symbols = {normalize_symbol(s) for s in current_pos.keys()} if current_pos else set()

    # 阶段1：清仓不在目标中的持仓
    for sym in current_symbols - target_symbols:
        log.info(f"SELL_REMOVED {sym}")
        order_target_percent(context, sym, 0.0)

    # 阶段2：调整至目标权重
    positions_map = get_normalized_positions_live()
    total_eq = float(context.portfolio.portfolio_value)

    def current_weight(sym: str) -> float:
        p = positions_map.get(sym)
        if p is None or total_eq <= 0:
            return 0.0
        try:
            return float(p.amount) * float(p.last_sale_price) / total_eq
        except Exception:
            return 0.0

    sell_orders, buy_orders = [], []
    for sym in sorted(all_targets.keys()):
        diff = all_targets[sym] - current_weight(sym)
        if abs(diff) < Config.REBALANCE_TOLERANCE:
            continue
        if diff < 0:
            sell_orders.append((sym, all_targets[sym]))
        else:
            buy_orders.append((sym, all_targets[sym]))

    for sym, tw in sell_orders:
        log.info(f"SELL {sym} target={tw:.4f}")
        order_target_percent(context, sym, tw)
    for sym, tw in buy_orders:
        log.info(f"BUY {sym} target={tw:.4f}")
        order_target_percent(context, sym, tw)


# =========================================================
# PTrade 生命周期
# =========================================================
def initialize(context):
    log.info("INIT")
    run_daily(context, strategy_main, time='14:50')

def before_trading_start(context, data):
    log.info("BEFORE_TRADING")

def after_trading_end(context, data):
    log.info("AFTER_TRADING")

def strategy_main(context):
    log.info("STRATEGY_MAIN")
    clear_cache()

    # 1. 一次性预计算所有资产的指标与横截面排序
    universe = precompute_universe()

    # 2. 排名与目标权重（仅计算一次）
    target_weights = get_target_weights(universe)

    # 3. 风险控制（风险因子计算一次，全链路复用）
    risk_factor = get_risk_scaling_factor(target_weights)
    risk_weights = get_risk_adjusted_weights(target_weights, risk_factor)
    cash_w = get_cash_weight(risk_weights)

    # 4. 日志记录
    log.info(f"STATE selected={list(target_weights.keys())} "
             f"risk_factor={risk_factor:.2f} cash={cash_w:.2f}")

    # 5. 执行再平衡
    rebalance(context, risk_weights, cash_w)
    return True