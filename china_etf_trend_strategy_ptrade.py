import math


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

# Full Universe

ETF_UNIVERSE = RISK_ETFS + [CASH_ETF]

# Indicator Configuration

MAX_LOOKBACK = 252

RETURN_WINDOWS = (20, 60, 120, 250,)

ATR_LOOKBACK = 20

LIQUIDITY_LOOKBACK = 60

QUALITY_LOOKBACK = 120

MOMENTUM_WEIGHTS = {20: 0.05, 60: 0.15, 120: 0.30, 250: 0.50,}

MARKET_FILTER_INDEXES = (
"510300.SS",  # CSI300
"510500.SS",  # CSI500
"512100.SS",  # CSI1000
)

MA_SHORT = 50
MA_MID = 150
MA_LONG = 250

MARKET_EXPOSURE_MAP = {0: 0.00, 1: 0.50, 2: 0.80, 3: 1.00,}

MOMENTUM_SCORE_WEIGHT = 0.70
QUALITY_SCORE_WEIGHT = 0.20
LIQUIDITY_SCORE_WEIGHT = 0.10


MAX_PORTFOLIO_SIZE = 5
RANKING_TREND_MA = 200

TARGET_PORTFOLIO_RISK = 0.10

MAX_SINGLE_POSITION_WEIGHT = 0.25
MIN_SINGLE_POSITION_WEIGHT = 0.05

LOW_RISK_THRESHOLD = 0.80
HIGH_RISK_THRESHOLD = 1.00
EXTREME_RISK_THRESHOLD = 1.20

LOW_RISK_EXPOSURE = 1.00
HIGH_RISK_EXPOSURE = 0.90
EXTREME_RISK_EXPOSURE = 0.75
DEFENSIVE_EXPOSURE = 0.50

# Global Cache

GLOBAL_CACHE = {}

# Cache Utilities

def clear_cache():
    GLOBAL_CACHE.clear()


    log.info("PERF-001 cache cleared")

def cache_get(key):
    return GLOBAL_CACHE.get(key)


def cache_set(key, value):
    GLOBAL_CACHE[key] = value
    
# =========================================================
# IND-001 Return Calculation
# =========================================================

def calc_return(symbol, lookback,):
    
    cache_key = ("return", symbol, lookback,)

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    if lookback not in RETURN_WINDOWS:

        raise ValueError(f"Unsupported lookback: {lookback}")

    close = get_close(symbol, lookback + 1,)

    if len(close) < lookback + 1:

        return None

    start_price = close[0]
    end_price = close[-1]

    if start_price <= 0:

        return None

    result = end_price / start_price - 1.0

    cache_set(cache_key, result)

    return result
    
# =========================================================
# IND-002 Volatility Calculation
# =========================================================

def calc_volatility(symbol, lookback=60):

    cache_key = ("volatility", symbol, lookback,)

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    close = get_close(symbol, lookback + 1)

    if len(close) < lookback + 1:
        return None

    returns = []

    for i in range(1, len(close)):

        returns.append(close[i] / close[i - 1] - 1.0)

    if len(returns) < 2:
        return None

    mean_return = sum(returns) / len(returns)

    variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
    
    result = math.sqrt(variance) * math.sqrt(252)
    

    cache_set(cache_key, result,)

    return result
    
# =========================================================
# IND-003 Momentum Score
# =========================================================

def _percentile_rank(value, values,):
    """
    Cross-sectional percentile rank.

    Returns
    -------
    float
        0 ~ 1
    """

    if value is None:
        return None

    valid_values = [v for v in values if v is not None]

    if len(valid_values) <= 1:
        return 0.5

    valid_values.sort()

    rank = sum(1 for v in valid_values if v <= value)

    return (rank - 1) / (len(valid_values) - 1)


def calc_risk_adjusted_momentum(symbol, lookback,):
    """
    Return / Volatility
    """

    ret = calc_return(symbol, lookback,)

    vol = calc_volatility(symbol, 60,)

    if ret is None:
        return None

    if vol is None:
        return None

    if vol <= 0:
        return None

    return ret / vol


def calc_momentum_score(symbol,):
    """
    Final momentum score.

    Returns
    -------
    float
        0 ~ 1
    """

    total_score = 0.0

    for lookback in RETURN_WINDOWS:

        cross_section = []

        for etf in RISK_ETFS:

            cross_section.append(calc_risk_adjusted_momentum(etf, lookback,))

        raw_value = calc_risk_adjusted_momentum(symbol, lookback,)
        
        percentile = _percentile_rank(raw_value, cross_section,)

        if percentile is None:
            return None

        total_score += MOMENTUM_WEIGHTS[lookback] * percentile

    return total_score

    
# =========================================================
# IND-004 Trend Quality Score
# =========================================================

def calc_trend_quality_raw(symbol, lookback=QUALITY_LOOKBACK,):
    
    cache_key = ("trend_quality", symbol, lookback,)

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    close = get_close(symbol, lookback,)

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

    fitted = [y_mean + slope * (xi - x_mean) for xi in x]

    ss_total = sum((y - y_mean) ** 2 for y in log_prices)

    if ss_total <= 0:

        return None

    ss_residual = sum((log_prices[i] - fitted[i]) ** 2 for i in range(n))

    r_squared = 1.0 - ss_residual / ss_total

    result = slope * r_squared

    cache_set(cache_key, result,)

    return result
    

def calc_quality_score(symbol,):
    """
    Cross-sectional quality score.

    Returns
    -------
    float
        0 ~ 1
    """

    raw_values = []

    for etf in RISK_ETFS:

        raw_values.append(calc_trend_quality_raw(etf))

    raw_value = calc_trend_quality_raw(symbol)
    

    return _percentile_rank(raw_value,raw_values,)

    
# =========================================================
# IND-005 Liquidity Score
# =========================================================

def calc_adv60(symbol, lookback=LIQUIDITY_LOOKBACK,):

    cache_key = ("adv", symbol, lookback,)

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    turnover = get_turnover(symbol, lookback,)

    if turnover is None:
        return None

    if len(turnover) < lookback:
        return None

    result = sum(turnover) / len(turnover)
    

    cache_set(cache_key, result,)

    return result

def calc_liquidity_score(symbol,):
    """
    Cross-sectional liquidity score.

    Returns
    -------
    float
        0 ~ 1
    """

    cross_section = []

    for etf in RISK_ETFS:

        cross_section.append(calc_adv60(etf))

    raw_value = calc_adv60(symbol)

    return _percentile_rank(raw_value, cross_section,)
    
# =========================================================
# IND-006 ATR20
# =========================================================

def calc_true_range(high, low, prev_close,):
    """
    True Range.

    Returns
    -------
    float
    """

    return max(high - low, abs(high - prev_close), abs(low - prev_close),)

def calc_atr(symbol, lookback=ATR_LOOKBACK,):

    cache_key = ("atr", symbol, lookback,)

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    high = get_high(symbol, lookback + 1,)

    low = get_low(symbol, lookback + 1,)

    close = get_close(symbol, lookback + 1,)

    if len(high) < lookback + 1 or len(low) < lookback + 1 or len(close) < lookback + 1:
        return None

    tr_values = []

    for i in range(1, len(close)):

        tr = calc_true_range(high[i], low[i], close[i - 1],)

        tr_values.append(tr)

    if len(tr_values) == 0:
        return None

    result = sum(tr_values) / len(tr_values)
    

    cache_set(cache_key, result,)

    return result
    
def calc_atr_percent(symbol,):

    atr = calc_atr(symbol)

    close = get_close(symbol, 1,)

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

def calc_ma(symbol,period,):

    close = get_close(symbol, period,)
    
    if len(close) < period:
    
        return None
    
    return sum(close[-period:]) / float(period)
    


def is_bull_trend(symbol,):

    close = get_close(symbol, MA_LONG,)
    
    if len(close) < MA_LONG:
    
        return False
    
    latest_close = close[-1]
    
    ma50 = calc_ma(symbol, MA_SHORT,)
    
    ma150 = calc_ma(symbol, MA_MID,)
    
    ma250 = calc_ma(symbol, MA_LONG,)
    
    if ma50 is None or ma150 is None or ma250 is None:
        return False
    
    return latest_close > ma50 and ma50 > ma150 and ma150 > ma250

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

    score = calc_market_score()
    
    return MARKET_EXPOSURE_MAP.get(score, 0.0,)
    
# =========================================================
# RANK-001 Final Score
# =========================================================

def calc_final_score(symbol,):

    momentum_score = calc_momentum_score(symbol)
    
    quality_score =  calc_quality_score(symbol)
    
    liquidity_score = calc_liquidity_score(symbol)
    

    if momentum_score is None or quality_score is None or liquidity_score is None:
        return None

    return MOMENTUM_SCORE_WEIGHT * momentum_score + QUALITY_SCORE_WEIGHT * quality_score + LIQUIDITY_SCORE_WEIGHT * liquidity_score
    
def build_ranking_table():
    
    log.info("DEBUG build_ranking_table")

    cache_key = "ranking_table"

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    candidates = []

    for symbol in RISK_ETFS:

        score = calc_final_score(symbol)

        if score is None:
            continue

        candidates.append((symbol, score))

    candidates.sort(key=lambda x: x[1], reverse=True)

    cache_set(cache_key, candidates)

    return candidates

def get_ranked_etfs():

    return build_ranking_table()

# =========================================================
# RANK-002 ETF Selection
# =========================================================

def passes_ranking_filter(symbol):

    close = get_close(symbol, RANKING_TREND_MA,)

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

def calc_inverse_volatility_weights(symbols,):

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

def normalize_weights(weights,):

    if len(weights) == 0:
        return {}

    total = sum(weights.values())

    if total <= 0:
        return {}

    return {symbol: weight / total for symbol, weight in weights.items()}


def apply_max_position_constraint(weights,):

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

            log.error("No eligible symbols for weight redistribution.")

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


def apply_min_position_constraint(weights,):

    adjusted = {}

    for symbol, weight in weights.items():

        if weight >= MIN_SINGLE_POSITION_WEIGHT:
            adjusted[symbol] = weight

    return adjusted


def apply_position_constraints(weights,):

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
    
def get_target_weights():

    cache_key = "target_weights"

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    result = calc_target_weights()

    cache_set(cache_key, result)

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

    return {"position_count": len(weights), "portfolio_atr": calc_portfolio_atr(), "weighted_average_volatility": calc_weighted_average_volatility(),}

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
    

    market_factor = calc_market_exposure()
    
    final_factor = risk_factor * market_factor
    

    adjusted = {}

    for symbol, weight in weights.items():

        adjusted[symbol] = weight * final_factor
        
    return adjusted

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

def get_position_value(symbol):

    positions = get_positions()

    if positions is None:
        return 0.0

    position = positions.get(symbol)

    if position is None:
        return 0.0

    try:
        return float(position.amount) * float(position.last_sale_price)
        

    except Exception as e:

        log.info(f"GET_POSITION_VALUE_EXCEPTION=" f"{repr(e)}")

        return 0.0


def order_target_percent(context, symbol, target_percent):

    try:

        total_equity = float(context.portfolio.portfolio_value)

        target_value = total_equity * target_percent

        current_value = get_position_value(symbol)

        delta_value = target_value - current_value
        
        # Ignore tiny adjustments

        if abs(delta_value) < 100:
            return None

        return order_value(symbol, delta_value)

    except Exception as e:

        log.info(f"ORDER_TARGET_PERCENT_EXCEPTION=" f"{repr(e)}")

        return None
    
# =========================================================
# EXEC-002 Rebalance Engine
# =========================================================

def get_current_symbols():

    positions = get_positions()

    if positions is None:
        return set()

    return {normalize_symbol(symbol) for symbol in positions.keys()}

def get_target_symbols(weights, cash_weight):

    symbols = set()

    for symbol, weight in weights.items():

        if weight > 0:
            symbols.add(symbol)

    if cash_weight > 0:
        symbols.add(CASH_ETF)

    return symbols

def sell_removed_positions(context, target_symbols):

    current_symbols = get_current_symbols()

    symbols_to_sell = current_symbols - target_symbols
    
    for symbol in symbols_to_sell:
    
        order_target_percent(context, symbol, 0.0)
        
    return symbols_to_sell

def get_current_weight(context, symbol):

    total_equity = float(context.portfolio.portfolio_value)

    if total_equity <= 0:
        return 0.0

    value = get_position_value(symbol)

    return value / total_equity

def rebalance_portfolio(context, weights, cash_weight):

    target_weights = weights.copy()

    if cash_weight > 0:
        target_weights[CASH_ETF] = cash_weight

    current_symbols = get_current_symbols()

    all_symbols = current_symbols | set(target_weights.keys())

    sell_orders = []

    buy_orders = []

    for symbol in all_symbols:

        current_weight = get_current_weight(context, symbol)

        target_weight = target_weights.get(symbol, 0.0)

        if target_weight < current_weight:

            sell_orders.append((symbol, target_weight))

        elif target_weight > current_weight:

            buy_orders.append((symbol, target_weight))

    # Phase 1
    # Sell first

    for symbol, target_weight in sell_orders:

        order_target_percent(context, symbol, target_weight)

        log.info(f"SELL TARGET {symbol}: " f"{target_weight:.2%}")

    # Phase 2
    # Buy later

    for symbol, target_weight in buy_orders:

        order_target_percent(context, symbol, target_weight)

        log.info(f"BUY TARGET {symbol}: " f"{target_weight:.2%}")

    return True

def rebalance(context):

    try:

        risk_weights = calc_risk_adjusted_weights()

        cash_weight = get_cash_weight(risk_weights)

        target_symbols = get_target_symbols(risk_weights, cash_weight)

        log.info("STEP1 sell_removed_positions")

        sell_removed_positions(context, target_symbols)

        log.info("STEP2 rebalance_portfolio")

        rebalance_portfolio(context, risk_weights, cash_weight)

        log.info("STEP3 completed")

        return True

    except Exception as e:

        log.error("REBALANCE_EXCEPTION=" + repr(e))

        return False


# =========================================================
# MIG-001A PTrade Lifecycle
# =========================================================

def initialize(context):
    log.info("initialize()")
    
    run_daily(context, strategy_main, time='14:50')

def before_trading_start(context, data):
    log.info("before_trading_start()")
    

def after_trading_end(context, data):
    log.info("after_trading_end()")
            
def strategy_main(context):
    
    clear_cache()

    log.info("strategy_main()")

    rebalance(context)

    return True
    
def _get_history_field(symbol, field, count):

    cache_key = ("history", symbol, field, count)

    cached = cache_get(cache_key)

    if cached is not None:
        return cached

    try:

        data = get_history(count, '1d', field, symbol, fq=None, include=False)

        if data is None:

            result = []

            cache_set(cache_key, result)

            return result

        if hasattr(data, "values") and hasattr(data, "columns"):

            if field in data.columns:

                result = list(data[field].values)

                cache_set(cache_key, result)

                return result

            if len(data.columns) == 1:

                result = list(data.iloc[:, 0].values)

                cache_set(cache_key, result)

                return result

        if hasattr(data, "tolist"):

            result = data.tolist()

            cache_set(cache_key, result)

            return result

        result = list(data)

        cache_set(cache_key, result)

        return result

    except Exception as e:

        log.error("_get_history_field failed: " + str(e))

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