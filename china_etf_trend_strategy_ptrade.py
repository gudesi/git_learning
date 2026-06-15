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


# Full Universe

ETF_UNIVERSE = RISK_ETFS + [CASH_ETF]

# Indicator Configuration

RETURN_WINDOWS = (20, 60, 120, 250,)

ATR_LOOKBACK = 20

LIQUIDITY_LOOKBACK = 60

QUALITY_LOOKBACK = 120

MOMENTUM_WEIGHTS = {20: 0.05, 60: 0.15, 120: 0.30, 250: 0.50,}

# =========================================================
# IND-001 Return Calculation
# =========================================================

def calc_return(symbol, lookback,):
    """
    Calculate simple return.

    Parameters
    ----------
    symbol : str

    lookback : int
        20 / 60 / 120 / 250

    Returns
    -------
    float
    """

    if lookback not in RETURN_WINDOWS:

        raise ValueError(f"Unsupported lookback: {lookback}")

    close = get_close(symbol, lookback + 1,)

    if len(close) < lookback + 1:

        return None

    start_price = close[0]
    end_price = close[-1]

    if start_price <= 0:

        return None

    return (end_price / start_price - 1.0)
    
# =========================================================
# IND-002 Volatility Calculation
# =========================================================

def calc_volatility(symbol, lookback=60):

    close = get_close(symbol, lookback + 1)

    if len(close) < lookback + 1:
        return None

    returns = []

    for i in range(1, len(close)):

        returns.append(close[i] / close[i - 1] - 1.0)

    mean_return = sum(returns) / len(returns)
    
    variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)

    return (math.sqrt(variance) * math.sqrt(252))
    
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
    """
    Raw trend quality.

    Quality =
    Slope × R²

    Uses log-price regression.

    Returns
    -------
    float
    """

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

    return slope * r_squared
    

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
    """
    Average Daily Turnover.

    Returns
    -------
    float
    """

    turnover = get_turnover(symbol, lookback,)

    if turnover is None:
        return None

    if len(turnover) < lookback:
        return None

    return (sum(turnover) / len(turnover))

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
    """
    ATR20.

    Returns
    -------
    float
    """

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

    return sum(tr_values) / len(tr_values)
    

# =========================================================
# MIG-001A PTrade Lifecycle
# =========================================================

def initialize(context):
    log.info("MIG-001A initialize()")
    
    # validate_ptrade_environment(context)
    
    g.MAX_LOOKBACK = 252
    
    run_daily(context, daily_heartbeat, time='14:50')

def before_trading_start(context, data):
    log.info("MIG-001A before_trading_start()")
    

def after_trading_end(context, data):
    log.info("MIG-001A after_trading_end()")
    

            
def daily_heartbeat(context):
    log.info("daily_heartbeat()")
    
    # validate_data_interface()
    
    # validate_portfolio_snapshot(context)
    
    # validate_order_interface(context)
    
    # validate_turnover_api()
    
    # log.info("validate IND-001 return_20 " + str(calc_return('510300.SS', 20)))
    
    # log.info("validate IND-001 return_60 " + str(calc_return('510300.SS', 60)))
    
    # log.info("validate IND-002 calc_volatility " + str(calc_volatility('510300.SS')))
    
    # log.info("validate IND-006 calc_atr " + str(calc_atr('510300.SS')))
    
    # log.info("validate IND-005 calc_adv60 " + str(calc_adv60('510300.SS')))
    
    # log.info("validate IND-005 calc_liquidity_score " + str(calc_liquidity_score('510300.SS')))
    
    # log.info("validate IND-005 type of get_turnover " + str(type(get_turnover('510300.SS', 60))))
    
    # log.info("validate IND-004 calc_quality_score " + str(calc_quality_score('510300.SS')))
    
    # log.info("validate IND-003 calc_momentum_score " + str(calc_momentum_score('510300.SS')))
    
    
def _get_history_field(symbol, field, count):

    try:
        data = get_history(count, '1d', field, symbol, fq=None, include=False)

        if data is None:
            return []

        # DataFrame (has both values and columns)
        if hasattr(data, "values") and hasattr(data, "columns"):
            if field in data.columns:
                return list(data[field].values)
            if len(data.columns) == 1:
                return list(data.iloc[:, 0].values)

        # Series (has tolist method)
        if hasattr(data, "tolist"):
            return data.tolist()

        # Fallback: treat as list or other iterable
        return list(data)

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
    

    
# =========================================================
# DEBUG TOOLS
# =========================================================

# MIG-001B Environment Validation

def validate_ptrade_environment(context):
    """
    Validate PTrade runtime environment.
    """

    log.info("========== CONTEXT ==========")

    try:
        log.info(str(dir(context)))
    except Exception as e:
        log.error(str(e))

    log.info("========== PORTFOLIO ==========")

    try:
        log.info(str(dir(context.portfolio)))
    except Exception as e:
        log.error(str(e))
        
    try:
        log.info("cash=" + str(context.portfolio.cash))
        
    except Exception as e:
        log.error(str(e))
        
    try:
        log.info("total_value=" + str(context.portfolio.total_value))
        
    except Exception as e:
        log.error(str(e))
        
    try:
        log.info("positions=" + str(context.portfolio.positions))
        
    except Exception as e:
            log.error(str(e))
            
# MIG-002 Data Interface Validation
            
def validate_data_interface():

    symbol = '510300.SS'
    
    close = get_close(symbol, 252)
    
    print(len(close))

    close = get_close(symbol, 5)

    high = get_high(symbol, 5)

    low = get_low(symbol, 5)

    volume = get_volume(symbol, 5)

    log.info("close=" + str(close))
    log.info("high=" + str(high))
    log.info("low=" + str(low))
    log.info("volume=" + str(volume))
    
def validate_turnover_api():

    try:

        data = get_turnover('510300.SS', 5)

        log.info("TURNOVER TEST: " + str(data))
        
        log.info(type(data))
        
        if len(data) > 0:

            log.info("FIRST=" + str(data[0]))
        
            log.info("LAST=" + str(data[-1]))

        if data is not None:

            log.info("TURNOVER AVG: " + str(sum(data) / len(data)))

    except Exception as e:

        log.error("TURNOVER TEST FAILED: " + str(e))

# MIG-003A Portfolio Snapshot

def validate_portfolio_snapshot(context):

    portfolio = context.portfolio

    log.info("cash=" + str(portfolio.cash))

    log.info("total_value=" + str(portfolio.total_value))

    log.info("positions=" + str(portfolio.positions))
    
    order_target_value('510300.SS', 10000)
    
    positions = context.portfolio.positions

    for symbol in positions:
    
        pos = positions[symbol]
    
        log.info("symbol=" + str(symbol))
    
        log.info("type=" + str(type(pos)))
    
        log.info("dir=" + str(dir(pos)))
        
    log.info("positions_value=" + str(context.portfolio.positions_value))
    
    log.info("returns=" + str(context.portfolio.returns))
    
# MIG-004 Order Interface Validation

def validate_order_interface(context):

    symbol = '510300.SS'

    log.info("========== ORDER TEST ==========")

    try:

        o = order_target_value(symbol, 20000)

        log.info("order=" + str(o))

        log.info("type=" + str(type(o)))

        log.info("dir=" + str(dir(o)))

    except Exception as e:

        log.error("order_target_value: " + str(e))

    try:

        orders = get_open_orders()

        log.info("open_orders=" + str(orders))

    except Exception as e:

        log.error("get_open_orders: " + str(e))