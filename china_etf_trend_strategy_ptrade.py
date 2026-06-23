import math
from functools import wraps

# =========================================================
# Strategy Configuration
# =========================================================

# Cash ETF
CASH_ETF = "511880.SS"

# Broad Market ETFs
BROAD_ETFS = [
    "510300.SS",  # CSI 300
    "510500.SS",  # CSI 500
    "512100.SS",  # CSI 1000
    "563300.SS",  # CSI A500
    "159915.SZ",  # ChiNext
    "588000.SS",  # STAR50
    "510880.SS",  # Dividend
]

# Financial ETFs
FINANCIAL_ETFS = [
    "512880.SS",  # Securities
    "512800.SS",  # Banking
]

# Technology ETFs
TECH_ETFS = [
    "512480.SS",  # Semiconductor
    "159819.SZ",  # AI
    "562500.SS",  # Robotics
    "512980.SS",  # Media
    "516160.SS",  # New Energy
]

# Defense ETFs
DEFENSE_ETFS = [
    "512660.SS",
]

# Healthcare ETFs
HEALTHCARE_ETFS = [
    "512010.SS",
]

# Consumer ETFs
CONSUMER_ETFS = [
    "159928.SZ",
]

# Resource ETFs
RESOURCE_ETFS = [
    "512400.SS",  # Nonferrous Metals
    "518880.SS",  # Gold
    "515220.SS",  # Coal
]

# Risk ETF Universe
RISK_ETFS = (
    BROAD_ETFS
    + FINANCIAL_ETFS
    + TECH_ETFS
    + DEFENSE_ETFS
    + HEALTHCARE_ETFS
    + CONSUMER_ETFS
    + RESOURCE_ETFS
)

def normalize_symbol(symbol):
    if symbol.endswith(".XSHG"):
        return symbol.replace(".XSHG", ".SS")
    if symbol.endswith(".XSHE"):
        return symbol.replace(".XSHE", ".SZ")
    return symbol

# Indicator Configuration

RETURN_WINDOWS = (20, 60, 120, 250)
ATR_LOOKBACK = 20
LIQUIDITY_LOOKBACK = 60
QUALITY_LOOKBACK = 120
MOMENTUM_WEIGHTS = {20: 0.05, 60: 0.15, 120: 0.30, 250: 0.50}
MARKET_FILTER_INDEXES = (
    "510300.SS",  # CSI300
    "510500.SS",  # CSI500
    "512100.SS",  # CSI1000
)
MA_SHORT = 50
MA_MID = 100
MA_LONG = 200
MARKET_EXPOSURE_MAP = {0: 0.00, 1: 0.50, 2: 0.80, 3: 1.00}
MOMENTUM_SCORE_WEIGHT = 0.70
QUALITY_SCORE_WEIGHT = 0.20
LIQUIDITY_SCORE_WEIGHT = 0.10
MAX_PORTFOLIO_SIZE = 5
RANKING_TREND_MA = 200
TARGET_PORTFOLIO_RISK = 0.15
MAX_SINGLE_POSITION_WEIGHT = 0.25
MIN_SINGLE_POSITION_WEIGHT = 0.05
LOW_RISK_THRESHOLD = 0.80
HIGH_RISK_THRESHOLD = 1.00
EXTREME_RISK_THRESHOLD = 1.20
LOW_RISK_EXPOSURE = 1.00
HIGH_RISK_EXPOSURE = 0.90
EXTREME_RISK_EXPOSURE = 0.75
DEFENSIVE_EXPOSURE = 0.50
REBALANCE_TOLERANCE = 0.01
COMMISSION_BUFFER = 0.98

# Global Cache
GLOBAL_CACHE = {}

# Cache Decorator
def cached(prefix):
    """Decorator that caches function results in GLOBAL_CACHE.
    For functions with arguments, the cache key is (prefix, *args).
    For functions without arguments, the cache key is the prefix string itself.
    """
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

# Cache Utilities (kept for compatibility, though no longer directly used)
def clear_cache():
    GLOBAL_CACHE.clear()

def cache_get(key):
    return GLOBAL_CACHE.get(key)

def cache_set(key, value):
    GLOBAL_CACHE[key] = value

# =========================================================
# STRAT-001 Market Filter Diagnostics
# =========================================================

MARKET_SCORE_STATS = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
}

# =========================================================
# AUDIT Portfolio Exposure Audit
# =========================================================

AUDIT_DAYS = 0

AUDIT_CASH_SUM = 0.0

AUDIT_CASH_GT_50 = 0

AUDIT_CASH_GT_80 = 0

AUDIT_RISK_FACTOR_SUM = 0.0

AUDIT_MARKET_FACTOR_SUM = 0.0

AUDIT_FINAL_FACTOR_SUM = 0.0

AUDIT_VOL_SUM = 0.0
AUDIT_USAGE_SUM = 0.0

AUDIT_VOL_COUNT = 0
AUDIT_USAGE_COUNT = 0

# =========================================================
# IND-001 Return Calculation
# =========================================================
@cached("return")
def calc_return(symbol, lookback):
    if lookback not in RETURN_WINDOWS:
        raise ValueError(f"Unsupported lookback: {lookback}")
    close = get_close(symbol, lookback + 1)
    if len(close) < lookback + 1:
        return None
    start_price = close[0]
    end_price = close[-1]
    if start_price <= 0:
        return None
    result = end_price / start_price - 1.0
    return result

# =========================================================
# IND-002 Volatility Calculation
# =========================================================
@cached("volatility")
def calc_volatility(symbol, lookback=60):
    close = get_close(symbol, lookback + 1)
    if len(close) < lookback + 1:
        return None
    returns = [close[i] / close[i-1] - 1 for i in range(1, len(close))]
    if len(returns) < 2:
        return None
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
    result = math.sqrt(variance) * math.sqrt(252)
    return result

# =========================================================
# IND-003 Momentum Score
# =========================================================
@cached("momentum_cross_section")
def get_momentum_cross_section(lookback):
    result = [calc_risk_adjusted_momentum(etf, lookback) for etf in RISK_ETFS]
    return result

def _percentile_rank(value, values):
    if value is None:
        return None
    valid_values = [v for v in values if v is not None]
    if len(valid_values) <= 1:
        return 0.5
    valid_values.sort()
    rank = sum(1 for v in valid_values if v <= value)
    return (rank - 1) / (len(valid_values) - 1)

@cached("risk_adj_momentum")
def calc_risk_adjusted_momentum(symbol, lookback):
    ret = calc_return(symbol, lookback)
    vol = calc_volatility(symbol, 60)
    if ret is None or vol is None or vol <= 0:
        result = None
    else:
        result = ret / vol
    return result

def calc_momentum_score(symbol):
    total_score = 0.0
    for lookback in RETURN_WINDOWS:
        cross_section = get_momentum_cross_section(lookback)
        raw_value = calc_risk_adjusted_momentum(symbol, lookback)
        percentile = _percentile_rank(raw_value, cross_section)
        if percentile is None:
            return None
        total_score += MOMENTUM_WEIGHTS[lookback] * percentile
    return total_score

# =========================================================
# IND-004 Trend Quality Score
# =========================================================
@cached("quality_cross_section")
def get_quality_cross_section():
    result = [calc_trend_quality_raw(etf) for etf in RISK_ETFS]
    return result

@cached("trend_quality")
def calc_trend_quality_raw(symbol, lookback=QUALITY_LOOKBACK):
    close = get_close(symbol, lookback)
    if len(close) < lookback:
        return None
    if min(close) <= 0:
        return None
    log_prices = [math.log(price) for price in close]
    x = list(range(len(log_prices)))
    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(log_prices) / n
    numerator = sum((x[i] - x_mean) * (log_prices[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    if denominator == 0:
        return None
    slope = numerator / denominator
    ss_total = sum((y - y_mean) ** 2 for y in log_prices)
    if ss_total <= 0:
        return None
    ss_residual = sum((log_prices[i] - (y_mean + slope*(x[i]-x_mean))) ** 2 for i in range(n))
    r_squared = 1.0 - ss_residual / ss_total
    result = slope * r_squared
    return result

def calc_quality_score(symbol):
    cross_section = get_quality_cross_section()
    raw_value = calc_trend_quality_raw(symbol)
    return _percentile_rank(raw_value, cross_section)

# =========================================================
# IND-005 Liquidity Score
# =========================================================
@cached("liquidity_cross_section")
def get_liquidity_cross_section():
    result = [calc_adv60(etf) for etf in RISK_ETFS]
    return result

@cached("adv")
def calc_adv60(symbol, lookback=LIQUIDITY_LOOKBACK):
    turnover = get_turnover(symbol, lookback)
    if turnover is None:
        return None
    if len(turnover) < lookback:
        return None
    result = sum(turnover) / len(turnover)
    return result

def calc_liquidity_score(symbol):
    cross_section = get_liquidity_cross_section()
    raw_value = calc_adv60(symbol)
    return _percentile_rank(raw_value, cross_section)

# =========================================================
# IND-006 ATR20
# =========================================================
def calc_true_range(high, low, prev_close):
    """
    True Range.

    Returns
    -------
    float
    """
    return max(high - low, abs(high - prev_close), abs(low - prev_close))

@cached("atr")
def calc_atr(symbol, lookback=ATR_LOOKBACK):
    high = get_high(symbol, lookback + 1)
    low = get_low(symbol, lookback + 1)
    close = get_close(symbol, lookback + 1)
    if len(high) < lookback + 1 or len(low) < lookback + 1 or len(close) < lookback + 1:
        return None
    tr_values = [calc_true_range(high[i], low[i], close[i - 1]) for i in range(1, len(close))]
    if len(tr_values) == 0:
        return None
    result = sum(tr_values) / len(tr_values)
    return result

def calc_atr_percent(symbol):
    atr = calc_atr(symbol)
    close = get_close(symbol, 1)
    if atr is None:
        return None
    if len(close) == 0:
        return None
    if close[-1] <= 0:
        return None
    return atr / close[-1]

# =========================================================
# FILTER-001 Market Breadth
# =========================================================
@cached("ma")
def calc_ma(symbol, period):
    close = get_close(symbol, period)
    if len(close) < period:
        return None
    result = sum(close) / float(period)
    return result

def is_bull_trend(symbol):
    close = get_close(symbol, MA_LONG)
    if len(close) < MA_LONG:
        return False
    latest_close = close[-1]
    ma_short = calc_ma(symbol, MA_SHORT)
    ma_mid = calc_ma(symbol, MA_MID)
    ma_long = calc_ma(symbol, MA_LONG)
    if ma_short is None or ma_mid is None or ma_long is None:
        return False
    return latest_close > ma_short and ma_short > ma_mid and ma_mid > ma_long

def calc_market_score():
    score = 0
    for symbol in MARKET_FILTER_INDEXES:
        if is_bull_trend(symbol):
            score += 1
    return score

# =========================================================
# FILTER-002 Market Exposure
# =========================================================
def calc_market_exposure():
    return 1.0

# def calc_market_exposure():
#     score = calc_market_score()
#     if score in MARKET_SCORE_STATS:
#         MARKET_SCORE_STATS[score] += 1
#     return MARKET_EXPOSURE_MAP.get(score, 0.0)

@cached("market_exposure")
def get_market_exposure():
    result = calc_market_exposure()
    return result

# =========================================================
# RANK-001 Final Score
# =========================================================
def calc_final_score(symbol):
    momentum_score = calc_momentum_score(symbol)
    quality_score = calc_quality_score(symbol)
    liquidity_score = calc_liquidity_score(symbol)
    if momentum_score is None or quality_score is None or liquidity_score is None:
        return None
    return MOMENTUM_SCORE_WEIGHT * momentum_score + QUALITY_SCORE_WEIGHT * quality_score + LIQUIDITY_SCORE_WEIGHT * liquidity_score

@cached("ranking_table")
def build_ranking_table():
    candidates = []
    for symbol in RISK_ETFS:
        score = calc_final_score(symbol)
        if score is None:
            continue
        candidates.append((symbol, score))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates

# =========================================================
# RANK-002 ETF Selection
# =========================================================
def passes_ranking_filter(symbol):
    close = get_close(symbol, RANKING_TREND_MA)
    if len(close) < RANKING_TREND_MA:
        return False
    ma200 = sum(close) / float(RANKING_TREND_MA)
    return close[-1] > ma200

def get_selected_etfs():
    candidates = []
    for symbol, score in build_ranking_table():
        if passes_ranking_filter(symbol):
            candidates.append((symbol, score))
    return [symbol for symbol, score in candidates[:MAX_PORTFOLIO_SIZE]]

# =========================================================
# PORT-001 Position Sizing
# =========================================================
def calc_inverse_volatility_weights(symbols):
    risk_values = {}
    for symbol in symbols:
        atr_pct = calc_atr_percent(symbol)
        if atr_pct is None:
            continue
        if atr_pct <= 0:
            continue
        risk_values[symbol] = 1.0 / atr_pct
    if len(risk_values) == 0:
        return {}
    total_risk = sum(risk_values.values())
    return {symbol: value / total_risk for symbol, value in risk_values.items()}

def calc_weights():
    selected = get_selected_etfs()
    if len(selected) == 0:
        return {}
    return calc_inverse_volatility_weights(selected)

# =========================================================
# PORT-002 Portfolio Constraints
# =========================================================
def normalize_weights(weights):
    if len(weights) == 0:
        return {}
    total = sum(weights.values())
    if total <= 0:
        return {}
    return {symbol: weight / total for symbol, weight in weights.items()}

def apply_max_position_constraint(weights):
    if len(weights) == 0:
        return {}
    adjusted = weights.copy()
    max_iterations = 20
    for _ in range(max_iterations):
        excess_weight = 0.0
        # Step 1
        # Cap overweight positions
        for symbol in adjusted:
            weight = adjusted[symbol]
            if weight > MAX_SINGLE_POSITION_WEIGHT:
                excess_weight += (weight - MAX_SINGLE_POSITION_WEIGHT)
                adjusted[symbol] = MAX_SINGLE_POSITION_WEIGHT
        # Finished
        if excess_weight <= 1e-8:
            break
        # Step 2
        # Find positions that can absorb weight
        eligible_symbols = []
        for symbol, weight in adjusted.items():
            if weight < MAX_SINGLE_POSITION_WEIGHT:
                eligible_symbols.append(symbol)
        # Safety check
        if len(eligible_symbols) == 0:
            break
        eligible_total = sum(adjusted[symbol] for symbol in eligible_symbols)
        if eligible_total <= 0:
            equal_share = excess_weight / len(eligible_symbols)
            for symbol in eligible_symbols:
                adjusted[symbol] += equal_share
        else:
            for symbol in eligible_symbols:
                proportion = adjusted[symbol] / eligible_total
                adjusted[symbol] += excess_weight * proportion
    return adjusted

def apply_min_position_constraint(weights):
    adjusted = {}
    for symbol, weight in weights.items():
        if weight >= MIN_SINGLE_POSITION_WEIGHT:
            adjusted[symbol] = weight
    return adjusted

def apply_position_constraints(weights):
    if len(weights) == 0:
        return {}
    adjusted = weights.copy()
    max_iterations = 10
    for _ in range(max_iterations):
        previous = adjusted.copy()
        # Max position constraint
        adjusted = apply_max_position_constraint(adjusted)
        adjusted = normalize_weights(adjusted)
        # Min position constraint
        adjusted = apply_min_position_constraint(adjusted)
        adjusted = normalize_weights(adjusted)
        # Converged
        if all(abs(adjusted.get(symbol, 0) - previous.get(symbol, 0)) < 1e-8 for symbol in set(adjusted) | set(previous)):
            break
    return adjusted

def calc_target_weights():
    weights = calc_weights()
    if len(weights) == 0:
        return {}
    weights = apply_position_constraints(weights)
    return weights

@cached("target_weights")
def get_target_weights():
    result = calc_target_weights()
    return result

# =========================================================
# RISK-001 Portfolio Risk Engine
# =========================================================
def calc_portfolio_atr():
    weights = get_target_weights()
    if len(weights) == 0:
        return None
    total_risk = 0.0
    total_weight = 0.0
    for symbol, weight in weights.items():
        atr_pct = calc_atr_percent(symbol)
        if atr_pct is None:
            continue
        total_risk += atr_pct * weight
        total_weight += weight
    if total_weight <= 0:
        return None
    return total_risk / total_weight

def calc_weighted_average_volatility():
    weights = get_target_weights()
    if len(weights) == 0:
        return None
    total_vol = 0.0
    total_weight = 0.0
    for symbol, weight in weights.items():
        vol = calc_volatility(symbol)
        if vol is None:
            continue
        total_vol += vol * weight
        total_weight += weight
    if total_weight <= 0:
        return None
    return total_vol / total_weight

def get_portfolio_statistics():
    weights = get_target_weights()
    return {"position_count": len(weights), "portfolio_atr": calc_portfolio_atr(), "weighted_average_volatility": calc_weighted_average_volatility()}

def calc_risk_budget_usage():
    stats = get_portfolio_statistics()
    portfolio_vol = stats.get("weighted_average_volatility")
    if portfolio_vol is None:
        return None
    if TARGET_PORTFOLIO_RISK <= 0:
        return None
    return portfolio_vol / TARGET_PORTFOLIO_RISK

def get_risk_state():
    usage = calc_risk_budget_usage()
    if usage is None:
        return "UNKNOWN"
    if usage < 0.8:
        return "LOW"
    if usage < 1.0:
        return "NORMAL"
    return "HIGH"

# =========================================================
# RISK-002 Portfolio Risk Control
# =========================================================
def get_risk_scaling_factor():
    usage = calc_risk_budget_usage()
    if usage is None:
        return 1.0
    if usage < LOW_RISK_THRESHOLD:
        return LOW_RISK_EXPOSURE
    if usage < HIGH_RISK_THRESHOLD:
        return HIGH_RISK_EXPOSURE
    if usage < EXTREME_RISK_THRESHOLD:
        return EXTREME_RISK_EXPOSURE
    return DEFENSIVE_EXPOSURE

def get_risk_control_state():
    factor = get_risk_scaling_factor()
    if factor >= 1.0:
        return "FULL"
    if factor >= 0.90:
        return "REDUCED"
    if factor >= 0.75:
        return "HIGH_RISK"
    return "DEFENSIVE"

def calc_risk_adjusted_weights():
    weights = get_target_weights()
    if len(weights) == 0:
        return {}
    risk_factor = get_risk_scaling_factor()
    market_factor = get_market_exposure()
    final_factor = risk_factor * market_factor
    adjusted = {symbol: weight * final_factor for symbol, weight in weights.items()}
    return adjusted

@cached("risk_adjusted_weights")
def get_risk_adjusted_weights():
    result = calc_risk_adjusted_weights()
    return result

def get_cash_weight(weights):
    invested = sum(weights.values())
    cash = max(0.0, min(1.0, 1.0 - invested))
    if cash < 0.0001:
        cash = 0.0
    return cash

# =========================================================
# EXEC-001
# Order Mapping Layer
# =========================================================

@cached("positions")
def get_positions_cached():
    result = get_positions()
    return result

@cached("normalized_positions")
def get_normalized_positions():
    positions = get_positions_cached()
    result = {
        normalize_symbol(symbol): position
        for symbol, position in positions.items()
    }
    return result

def lookup_position(symbol):
    positions = get_normalized_positions()
    return positions.get(symbol)

def get_position_value(symbol):
    position = lookup_position(symbol)
    if position is None:
        return 0.0
    try:
        return (
            float(position.amount)
            * float(position.last_sale_price)
        )
    except Exception as e:
        log.info(
            f"GET_POSITION_VALUE_EXCEPTION={repr(e)}"
        )
        return 0.0

def order_target_percent(
    context,
    symbol,
    target_percent
):
    try:
        total_equity = float(
            context.portfolio.portfolio_value
        )
        # EXEC-001
        # 留出手续费和滑点缓冲
        target_value = (
            total_equity
            * target_percent
            * COMMISSION_BUFFER
        )
        current_value = get_position_value(symbol)
        delta_value = (
            target_value
            - current_value
        )
        log.info(
            f"ORDER_DEBUG "
            f"{symbol} "
            f"target={target_percent:.4f} "
            f"current={current_value:.2f} "
            f"target_value={target_value:.2f} "
            f"delta={delta_value:.2f}"
        )
        # EXEC-001
        # 仅过滤买入小单
        if delta_value > 0:
            if symbol == CASH_ETF:
                threshold = max(
                    total_equity * 0.005,
                    12000
                )
            else:
                threshold = 1000
            if delta_value < threshold:
                log.info(
                    f"ORDER_SKIPPED "
                    f"{symbol} "
                    f"delta={delta_value:.2f} "
                    f"threshold={threshold:.2f}"
                )
                return None
        return order_value(
            symbol,
            delta_value
        )
    except Exception as e:
        log.info(
            f"ORDER_TARGET_PERCENT_EXCEPTION={repr(e)}"
        )
        return None

# =========================================================
# EXEC-002
# Rebalance Engine
# =========================================================

def get_current_symbols():
    positions = get_positions_cached()
    if positions is None:
        return set()
    return {
        normalize_symbol(symbol)
        for symbol in positions.keys()
    }

def get_target_symbols(
    weights,
    cash_weight
):
    symbols = set()
    for symbol, weight in weights.items():
        if weight > 0:
            symbols.add(symbol)
    if cash_weight > 0:
        symbols.add(CASH_ETF)
    return symbols

def sell_removed_positions(
    context,
    target_symbols
):
    current_symbols = get_current_symbols()
    symbols_to_sell = (
        current_symbols
        - target_symbols
    )
    log.info(
        f"CURRENT={current_symbols}"
    )
    log.info(
        f"TARGET={target_symbols}"
    )
    log.info(
        f"REMOVE={symbols_to_sell}"
    )
    for symbol in symbols_to_sell:
        log.info(
            f"SELL_REMOVED {symbol}"
        )
        order_target_percent(
            context,
            symbol,
            0.0
        )
    return symbols_to_sell

def get_current_weight(
    context,
    symbol
):
    total_equity = float(
        context.portfolio.portfolio_value
    )
    if total_equity <= 0:
        return 0.0
    value = get_position_value(symbol)
    return value / total_equity

def rebalance_portfolio(
    context,
    weights,
    cash_weight
):
    target_weights = weights.copy()
    if cash_weight > 0:
        target_weights[CASH_ETF] = cash_weight
    all_symbols = set(
        target_weights.keys()
    )
    sell_orders = []
    buy_orders = []
    for symbol in sorted(all_symbols):
        current_weight = get_current_weight(
            context,
            symbol
        )
        target_weight = (
            target_weights.get(
                symbol,
                0.0
            )
        )
        difference = (
            target_weight
            - current_weight
        )
        if abs(difference) < REBALANCE_TOLERANCE:
            continue
        if difference < 0:
            sell_orders.append(
                (
                    symbol,
                    target_weight
                )
            )
        else:
            buy_orders.append(
                (
                    symbol,
                    target_weight
                )
            )
    # ====================================
    # Phase 1
    # Sell First
    # ====================================
    for symbol, target_weight in sell_orders:
        log.info(
            f"SELL {symbol} "
            f"target={target_weight:.4f}"
        )
        order_target_percent(
            context,
            symbol,
            target_weight
        )
    # ====================================
    # Phase 2
    # Buy Second
    # ====================================
    for symbol, target_weight in buy_orders:
        log.info(
            f"BUY {symbol} "
            f"target={target_weight:.4f}"
        )
        order_target_percent(
            context,
            symbol,
            target_weight
        )
    return True

def rebalance(context):
    try:
        risk_weights = (
            get_risk_adjusted_weights()
        )
        cash_weight = (
            get_cash_weight(
                risk_weights
            )
        )
        target_symbols = (
            get_target_symbols(
                risk_weights,
                cash_weight
            )
        )
        sell_removed_positions(
            context,
            target_symbols
        )
        rebalance_portfolio(
            context,
            risk_weights,
            cash_weight
        )
        return True
    except Exception as e:
        log.error(
            "REBALANCE_EXCEPTION="
            + repr(e)
        )
        return False

# =========================================================
# MIG-001A PTrade Lifecycle
# =========================================================
def initialize(context):
    log.info("LIFECYCLE initialize")
    run_daily(context, strategy_main, time='14:50')

def before_trading_start(context, data):
    log.info("LIFECYCLE before_trading_start")

def after_trading_end(context, data):
    log.info("LIFECYCLE after_trading_end")

    if AUDIT_DAYS % 100 == 0:
        print_audit_summary()

def strategy_main(context):
    log.info("LIFECYCLE strategy_main")
    clear_cache()

    audit_portfolio_state()
    
    rebalance(context)
    return True

@cached("history")
def _get_history_field(symbol, field, count):
    try:
        data = get_history(count, '1d', field, symbol, fq='post', include=False)
        if data is None:
            result = []
            return result
        if hasattr(data, "values") and hasattr(data, "columns"):
            if field in data.columns:
                result = list(data[field].values)
                return result
            if len(data.columns) == 1:
                result = list(data.iloc[:, 0].values)
                return result
        if hasattr(data, "tolist"):
            result = data.tolist()
            return result
        result = list(data)
        return result
    except Exception as e:
        log.error(f"GET_HISTORY_FAILED symbol={symbol} field={field} count={count} error={repr(e)}")
        return []

def get_close(symbol, count):
    return _get_history_field(symbol, 'close', count)

def get_high(symbol, count):
    return _get_history_field(symbol, 'high', count)

def get_low(symbol, count):
    return _get_history_field(symbol, 'low', count)

def get_volume(symbol, count):
    return _get_history_field(symbol, 'volume', count)

def get_turnover(symbol, count):
    return _get_history_field(symbol, 'money', count)

# =========================================================
# DEBUG Portfolio Audit
# =========================================================

# =========================================================
# AUDIT Portfolio Exposure Audit
# =========================================================

def audit_portfolio_state():

    global AUDIT_DAYS

    global AUDIT_CASH_SUM

    global AUDIT_CASH_GT_50

    global AUDIT_CASH_GT_80

    global AUDIT_RISK_FACTOR_SUM

    global AUDIT_MARKET_FACTOR_SUM

    global AUDIT_FINAL_FACTOR_SUM

    global AUDIT_VOL_SUM

    global AUDIT_USAGE_SUM

    global AUDIT_VOL_COUNT

    global AUDIT_USAGE_COUNT

    try:

        risk_factor = get_risk_scaling_factor()

        market_factor = get_market_exposure()

        final_factor = (
            risk_factor
            * market_factor
        )

        adjusted_weights = (
            get_risk_adjusted_weights()
        )

        cash_weight = get_cash_weight(
            adjusted_weights
        )

        AUDIT_DAYS += 1

        AUDIT_CASH_SUM += cash_weight

        AUDIT_RISK_FACTOR_SUM += risk_factor

        AUDIT_MARKET_FACTOR_SUM += market_factor

        AUDIT_FINAL_FACTOR_SUM += final_factor

        if cash_weight > 0.50:
            AUDIT_CASH_GT_50 += 1

        if cash_weight > 0.80:
            AUDIT_CASH_GT_80 += 1

        portfolio_vol = (
            calc_weighted_average_volatility()
        )

        usage = (
            calc_risk_budget_usage()
        )

        if portfolio_vol is not None:
            AUDIT_VOL_SUM += portfolio_vol
            AUDIT_VOL_COUNT += 1

        if usage is not None:
            AUDIT_USAGE_SUM += usage
            AUDIT_USAGE_COUNT += 1

    except Exception as e:

        log.info(
            f"AUDIT_EXCEPTION={repr(e)}"
        )

def print_audit_summary():

    if AUDIT_DAYS <= 0:
        return

    avg_cash = (
        AUDIT_CASH_SUM
        / AUDIT_DAYS
    )

    avg_risk_factor = (
        AUDIT_RISK_FACTOR_SUM
        / AUDIT_DAYS
    )

    avg_market_factor = (
        AUDIT_MARKET_FACTOR_SUM
        / AUDIT_DAYS
    )

    avg_final_factor = (
        AUDIT_FINAL_FACTOR_SUM
        / AUDIT_DAYS
    )

    pct_cash_gt_50 = (
        AUDIT_CASH_GT_50
        / AUDIT_DAYS
        * 100
    )

    pct_cash_gt_80 = (
        AUDIT_CASH_GT_80
        / AUDIT_DAYS
        * 100
    )

    log.info(
        "========== AUDIT SUMMARY =========="
    )

    log.info(
        f"AUDIT_DAYS={AUDIT_DAYS}"
    )

    log.info(
        f"AVG_CASH_WEIGHT={avg_cash:.4f}"
    )

    log.info(
        f"CASH_GT_50_PCT={pct_cash_gt_50:.2f}"
    )

    log.info(
        f"CASH_GT_80_PCT={pct_cash_gt_80:.2f}"
    )

    log.info(
        f"AVG_RISK_FACTOR={avg_risk_factor:.4f}"
    )

    log.info(
        f"AVG_MARKET_FACTOR={avg_market_factor:.4f}"
    )

    log.info(
        f"AVG_FINAL_FACTOR={avg_final_factor:.4f}"
    )

    log.info(
        "==================================="
    )

    avg_vol = (
        AUDIT_VOL_SUM
        / AUDIT_VOL_COUNT
        if AUDIT_VOL_COUNT > 0
        else 0
    )

    avg_usage = (
        AUDIT_USAGE_SUM
        / AUDIT_USAGE_COUNT
        if AUDIT_USAGE_COUNT > 0
        else 0
    )

    log.info(
        f"AVG_PORTFOLIO_VOL={avg_vol:.4f}"
    )

    log.info(
        f"AVG_RISK_USAGE={avg_usage:.4f}"
    )