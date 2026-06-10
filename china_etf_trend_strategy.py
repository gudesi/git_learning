# =========================================================
# ETF Universe Definition
# DATA-001
# =========================================================

# ---------------------------------------------------------
# Cash ETF
# ---------------------------------------------------------

CASH_ETF = "511880"


# ---------------------------------------------------------
# Broad Market ETFs
# ---------------------------------------------------------

BROAD_ETFS = [
    "510300",  # CSI 300
    "510500",  # CSI 500
    "512100",  # CSI 1000
    "563300",  # CSI A500
    "159915",  # ChiNext
    "588000",  # STAR50
    "510880",  # Dividend
]


# ---------------------------------------------------------
# Financial ETFs
# ---------------------------------------------------------

FINANCIAL_ETFS = [
    "512880",  # Securities
    "512800",  # Banking
]


# ---------------------------------------------------------
# Technology ETFs
# ---------------------------------------------------------

TECH_ETFS = [
    "512480",  # Semiconductor
    "159819",  # AI
    "562500",  # Robotics
    "512980",  # Media
    "516160",  # New Energy
]


# ---------------------------------------------------------
# Defense ETFs
# ---------------------------------------------------------

DEFENSE_ETFS = [
    "512660",  # Military
]


# ---------------------------------------------------------
# Healthcare ETFs
# ---------------------------------------------------------

HEALTHCARE_ETFS = [
    "512010",  # Healthcare
]


# ---------------------------------------------------------
# Consumer ETFs
# ---------------------------------------------------------

CONSUMER_ETFS = [
    "159928",  # Consumer
]


# ---------------------------------------------------------
# Resource ETFs
# ---------------------------------------------------------

RESOURCE_ETFS = [
    "512400",  # Nonferrous Metals
    "518880",  # Gold
    "515220",  # Coal
]


# ---------------------------------------------------------
# Risk ETF Universe
# ---------------------------------------------------------

RISK_ETFS = (
    BROAD_ETFS
    + FINANCIAL_ETFS
    + TECH_ETFS
    + DEFENSE_ETFS
    + HEALTHCARE_ETFS
    + CONSUMER_ETFS
    + RESOURCE_ETFS
)


# ---------------------------------------------------------
# Full Universe
# ---------------------------------------------------------

ETF_UNIVERSE = RISK_ETFS + [CASH_ETF]

# ETF Category Mapping

ETF_CATEGORY_MAP = {

    # Broad
    "510300": "broad",
    "510500": "broad",
    "512100": "broad",
    "563300": "broad",
    "159915": "broad",
    "588000": "broad",
    "510880": "broad",

    # Financial
    "512880": "financial",
    "512800": "financial",

    # Technology
    "512480": "technology",
    "159819": "technology",
    "562500": "technology",
    "512980": "technology",
    "516160": "technology",

    # Defense
    "512660": "defense",

    # Healthcare
    "512010": "healthcare",

    # Consumer
    "159928": "consumer",

    # Resource
    "512400": "resource",
    "518880": "resource",
    "515220": "resource",

    # Cash
    "511880": "cash",
}

# Asset Class Mapping

ASSET_CLASS_MAP = ETF_CATEGORY_MAP.copy()

# ETF Name Mapping 

ETF_NAME_MAP = {

    "510300": "CSI300 ETF",
    "510500": "CSI500 ETF",
    "512100": "CSI1000 ETF",
    "563300": "CSI A500 ETF",
    "159915": "ChiNext ETF",
    "588000": "STAR50 ETF",
    "510880": "Dividend ETF",

    "512880": "Securities ETF",
    "512800": "Banking ETF",

    "512480": "Semiconductor ETF",
    "159819": "AI ETF",
    "562500": "Robotics ETF",
    "512980": "Media ETF",
    "516160": "New Energy ETF",

    "512660": "Defense ETF",

    "512010": "Healthcare ETF",

    "159928": "Consumer ETF",

    "512400": "Nonferrous Metals ETF",
    "518880": "Gold ETF",
    "515220": "Coal ETF",

    "511880": "Cash ETF",
}

# =========================================================
# DATA-001 Validation
# =========================================================

EXPECTED_RISK_ETF_COUNT = 20
EXPECTED_TOTAL_ETF_COUNT = 21


def validate_universe():
    """
    Validate ETF universe configuration.

    Returns
    -------
    bool
        True if all validations pass.
    """

    # -----------------------------------------------------
    # Count Validation
    # -----------------------------------------------------

    assert len(RISK_ETFS) == EXPECTED_RISK_ETF_COUNT, (
        f"Expected {EXPECTED_RISK_ETF_COUNT} risk ETFs, "
        f"got {len(RISK_ETFS)}"
    )

    assert len(ETF_UNIVERSE) == EXPECTED_TOTAL_ETF_COUNT, (
        f"Expected {EXPECTED_TOTAL_ETF_COUNT} ETFs, "
        f"got {len(ETF_UNIVERSE)}"
    )

    # -----------------------------------------------------
    # Duplicate Validation
    # -----------------------------------------------------

    assert len(set(ETF_UNIVERSE)) == len(ETF_UNIVERSE), (
        "Duplicate ETF codes found"
    )

    # -----------------------------------------------------
    # Cash ETF Validation
    # -----------------------------------------------------

    assert CASH_ETF in ETF_UNIVERSE, (
        "Cash ETF missing from ETF_UNIVERSE"
    )

    assert CASH_ETF not in RISK_ETFS, (
        "Cash ETF should not appear in RISK_ETFS"
    )

    # -----------------------------------------------------
    # Mapping Validation
    # -----------------------------------------------------

    for symbol in ETF_UNIVERSE:

        assert symbol in ETF_CATEGORY_MAP, (
            f"{symbol} missing from ETF_CATEGORY_MAP"
        )

        assert symbol in ETF_NAME_MAP, (
            f"{symbol} missing from ETF_NAME_MAP"
        )

        assert symbol in ASSET_CLASS_MAP, (
            f"{symbol} missing from ASSET_CLASS_MAP"
        )

    return True

# =========================================================
# DATA-002
# Configuration Management
# =========================================================

# ---------------------------------------------------------
# Data Layer
# ---------------------------------------------------------

MAX_LOOKBACK = 252
MIN_HISTORY = 252

# ---------------------------------------------------------
# Trend Following
# ---------------------------------------------------------

RETURN_LOOKBACKS = (
    20,
    60,
    120,
    250,
)

# ---------------------------------------------------------
# Volatility
# ---------------------------------------------------------

ATR_LOOKBACK = 20

# ---------------------------------------------------------
# Portfolio Construction
# ---------------------------------------------------------

MAX_POSITIONS = 5

# ---------------------------------------------------------
# Risk Management
# ---------------------------------------------------------

TARGET_PORTFOLIO_RISK = 0.10

MAX_SINGLE_POSITION_WEIGHT = 0.25
MIN_SINGLE_POSITION_WEIGHT = 0.05

# ---------------------------------------------------------
# Rebalance
# ---------------------------------------------------------

REBALANCE_FREQUENCY = "monthly"

# ---------------------------------------------------------
# Liquidity
# ---------------------------------------------------------

MIN_DAILY_TURNOVER = 50_000_000

# =========================================================
# DATA-002 Validation
# =========================================================

def validate_config():

    assert MAX_LOOKBACK > 0
    assert MIN_HISTORY > 0

    assert MIN_HISTORY <= MAX_LOOKBACK

    assert len(RETURN_LOOKBACKS) > 0

    for lookback in RETURN_LOOKBACKS:
        assert lookback > 0

    assert RETURN_LOOKBACKS == tuple(
        sorted(RETURN_LOOKBACKS)
    )
    
    assert ATR_LOOKBACK > 0

    assert MAX_POSITIONS > 0

    assert (
        0 < TARGET_PORTFOLIO_RISK < 1
    )

    assert (
        0 < MIN_SINGLE_POSITION_WEIGHT
        <= MAX_SINGLE_POSITION_WEIGHT
        <= 1
    )

    assert REBALANCE_FREQUENCY in {
        "daily",
        "weekly",
        "monthly",
    }

    assert MIN_DAILY_TURNOVER > 0

    return True

# ============================================================
# FIX-001B：增加日志接口 Logging
# ============================================================

def log_info(message):
    """
    Log info message.
    """

    print(f"[INFO] {message}")


def log_warning(message):
    """
    Log warning message.
    """

    print(f"[WARNING] {message}")


def log_error(code, message):
    """
    Log error message.
    """

    print(
        f"[ERROR] {code}: {message}"
    )

def _test_logging():
    """
    Logging validation.
    """

    log_info("INFO TEST")
    log_warning("WARNING TEST")
    log_error(
        "TEST",
        "ERROR TEST"
    )

    print(
        "LOGGING validation passed."
    )

# =========================================================
# STATE-001
# Strategy State Management
# =========================================================

from copy import deepcopy

# ---------------------------------------------------------
# Default Position State
# ---------------------------------------------------------

DEFAULT_POSITION_STATE = {
    "entry_price": None,
    "entry_date": None,
    "stop_price": None,
    "highest_close": None,
}

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------

def init_strategy_state(context):
    """
    Initialize strategy state container.

    Parameters
    ----------
    context : object
        PTrade context object.
    """

    if not hasattr(context, "strategy_state"):
        context.strategy_state = {}

# ---------------------------------------------------------
# State Access
# ---------------------------------------------------------

def get_position_state(context, symbol):
    """
    Get state for a symbol.

    Automatically creates state if missing.
    """

    init_strategy_state(context)

    if symbol not in context.strategy_state:
        context.strategy_state[symbol] = deepcopy(
            DEFAULT_POSITION_STATE
        )

    return context.strategy_state[symbol]

# ---------------------------------------------------------
# Entry Registration
# ---------------------------------------------------------

def register_entry(
    context,
    symbol,
    entry_price,
    entry_date,
    stop_price=None,
):
    """
    Create/update position state after entry.
    """

    state = get_position_state(context, symbol)

    state["entry_price"] = float(entry_price)
    state["entry_date"] = str(entry_date)
    state["stop_price"] = stop_price
    state["highest_close"] = float(entry_price)

# ---------------------------------------------------------
# Highest Close Update
# ---------------------------------------------------------

def update_highest_close(
    context,
    symbol,
    latest_close,
):
    """
    Update highest close since entry.
    """

    state = get_position_state(context, symbol)

    current_high = state["highest_close"]

    if current_high is None:
        state["highest_close"] = float(latest_close)
        return

    state["highest_close"] = max(
        current_high,
        float(latest_close),
    )

# ---------------------------------------------------------
# Stop Price Update
# ---------------------------------------------------------

def update_stop_price(
    context,
    symbol,
    stop_price,
):
    """
    Update stop price.
    """

    state = get_position_state(context, symbol)

    state["stop_price"] = float(stop_price)

# ---------------------------------------------------------
# Position Exit
# ---------------------------------------------------------

def clear_position_state(
    context,
    symbol,
):
    """
    Remove state after full exit.
    """

    init_strategy_state(context)

    if symbol in context.strategy_state:
        del context.strategy_state[symbol]

# ---------------------------------------------------------
# State Validation
# ---------------------------------------------------------

def validate_strategy_state(context):
    """
    Validate strategy state structure.
    """

    init_strategy_state(context)

    required_fields = {
        "entry_price",
        "entry_date",
        "stop_price",
        "highest_close",
    }

    for symbol, state in context.strategy_state.items():

        missing = required_fields - set(state.keys())

        assert not missing, (
            f"{symbol} missing fields: {missing}"
        )

    return True

# ---------------------------------------------------------
# Daily State Maintenance
# ---------------------------------------------------------

def update_daily_state(
    context,
    symbol,
    latest_close,
):
    """
    Daily maintenance hook.

    Called after market close.
    """

    update_highest_close(
        context,
        symbol,
        latest_close,
    )

# =========================================================
# STATE-001 Self Test
# =========================================================

def _test_state_management():

    class MockContext:
        pass

    context = MockContext()

    init_strategy_state(context)

    register_entry(
        context=context,
        symbol="510300",
        entry_price=4.20,
        entry_date="2026-06-05",
        stop_price=3.80,
    )

    state = get_position_state(
        context,
        "510300",
    )

    assert state["entry_price"] == 4.20
    assert state["highest_close"] == 4.20

    update_highest_close(
        context,
        "510300",
        4.50,
    )

    assert (
        context.strategy_state["510300"]["highest_close"]
        == 4.50
    )

    update_stop_price(
        context,
        "510300",
        4.00,
    )

    assert (
        context.strategy_state["510300"]["stop_price"]
        == 4.00
    )

    validate_strategy_state(context)

    clear_position_state(
        context,
        "510300",
    )

    assert (
        "510300"
        not in context.strategy_state
    )

    return True

# ============================================================
# FIX-001A：增加 PTrade Stub  PTrade Platform Stubs
# ============================================================

def get_history(*args, **kwargs):
    """
    PTrade API Stub.

    Real implementation is provided by
    PTrade runtime environment.

    This stub exists only for:

    - VSCode type checking
    - Local development
    - Unit testing

    """
    # TODO:
    # Replace with real PTrade API
    # during production deployment.

    raise NotImplementedError(
        "get_history() requires PTrade runtime."
    )

# =========================================================
# DATA-003
# Data Access Layer
# =========================================================

# ---------------------------------------------------------
# Internal History Fetcher
# ---------------------------------------------------------

def _get_history_field(
    symbol,
    field,
    count=None,
):
    """
    Unified historical data access.

    Parameters
    ----------
    symbol : str
        ETF code.

    field : str
        close/high/low/volume/amount

    count : int
        History length.

    Returns
    -------
    list[float]
    """

    if count is None:
        count = MAX_LOOKBACK

    try:

        data = get_history(
            security=symbol,
            field=field,
            count=count,
        )

        if data is None:
            return []

        values = list(data)

        return values

    except Exception as e:

        log_warning("History fetch failed")

        return []

# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_history(
    data,
    min_length=None,
):
    """
    Validate historical data.
    """

    if min_length is None:
        min_length = MIN_HISTORY

    if data is None:
        return False

    if len(data) < min_length:
        return False

    return True

# ---------------------------------------------------------
# Close
# ---------------------------------------------------------

def get_close(
    symbol,
    count=None,
):
    """
    Get close prices.
    """

    return _get_history_field(
        symbol=symbol,
        field="close",
        count=count,
    )

# ---------------------------------------------------------
# High
# ---------------------------------------------------------

def get_high(
    symbol,
    count=None,
):
    """
    Get high prices.
    """

    return _get_history_field(
        symbol=symbol,
        field="high",
        count=count,
    )

# ---------------------------------------------------------
# Low
# ---------------------------------------------------------

def get_low(
    symbol,
    count=None,
):
    """
    Get low prices.
    """

    return _get_history_field(
        symbol=symbol,
        field="low",
        count=count,
    )

# ---------------------------------------------------------
# Volume
# ---------------------------------------------------------

def get_volume(
    symbol,
    count=None,
):
    """
    Get volume series.
    """

    return _get_history_field(
        symbol=symbol,
        field="volume",
        count=count,
    )

# ---------------------------------------------------------
# Turnover
# ---------------------------------------------------------

def get_turnover(
    symbol,
    count=None,
):
    """
    Get turnover(amount) series.
    """

    return _get_history_field(
        symbol=symbol,
        field="amount",
        count=count,
    )

# ---------------------------------------------------------
# Data Bundle
# ---------------------------------------------------------

def get_price_bundle(
    symbol,
    count=None,
):
    """
    Fetch all required fields once.

    Returns
    -------
    dict
    """

    return {
        "close": get_close(symbol, count),
        "high": get_high(symbol, count),
        "low": get_low(symbol, count),
        "volume": get_volume(symbol, count),
        "amount": get_turnover(symbol, count),
    }

# ---------------------------------------------------------
# ETF Eligibility Check
# ---------------------------------------------------------

def is_data_available(
    symbol,
):
    """
    Check whether ETF has enough history.

    Returns
    -------
    bool
    """

    close = get_close(
        symbol,
        MAX_LOOKBACK,
    )

    return validate_history(close)

# ---------------------------------------------------------
# Universe Filter
# ---------------------------------------------------------

def get_valid_etfs():
    """
    Return ETFs with sufficient history.
    """

    valid_symbols = []

    for symbol in RISK_ETFS:

        if is_data_available(symbol):
            valid_symbols.append(symbol)

    return valid_symbols

# =========================================================
# DATA-003 Self Test
# =========================================================

def _test_data_layer():

    sample_symbol = ETF_UNIVERSE[0]

    close = get_close(sample_symbol)
    high = get_high(sample_symbol)
    low = get_low(sample_symbol)
    volume = get_volume(sample_symbol)
    amount = get_turnover(sample_symbol)

    assert isinstance(close, list)
    assert isinstance(high, list)
    assert isinstance(low, list)
    assert isinstance(volume, list)
    assert isinstance(amount, list)

    return True

# =========================================================
# DATA-004
# Portfolio Access Layer
# =========================================================

def get_total_equity(context):
    """
    Get total portfolio equity.

    Returns
    -------
    float
    """

    try:

        return float(
            context.portfolio.portfolio_value
        )

    except Exception as e:

        log_error(
            "GET_TOTAL_EQUITY_FAILED",
            str(e)
        )

        return 0.0


def get_available_cash(context):
    """
    Get available cash.

    Returns
    -------
    float
    """

    try:

        return float(
            context.portfolio.cash
        )

    except Exception as e:

        log_error(
            "GET_AVAILABLE_CASH_FAILED",
            str(e)
        )

        return 0.0


def get_position_value(context):
    """
    Get total market value
    of all positions.

    Returns
    -------
    float
    """

    try:

        return float(
            context.portfolio.positions_value
        )

    except Exception as e:

        log_error(
            "GET_POSITION_VALUE_FAILED",
            str(e)
        )

        return 0.0


def get_positions(context):
    """
    Get all positions.

    Returns
    -------
    dict
        symbol -> Position
    """

    try:

        return (
            context.portfolio.positions
            or {}
        )

    except Exception as e:

        log_error(
            "GET_POSITIONS_FAILED",
            str(e)
        )

        return {}


def get_position(context, symbol):
    """
    Get single position.

    Parameters
    ----------
    symbol : str

    Returns
    -------
    Position | None
    """

    positions = get_positions(context)

    return positions.get(symbol)


def has_position(context, symbol):
    """
    Check whether
    position exists.

    Returns
    -------
    bool
    """

    position = get_position(
        context,
        symbol
    )

    if position is None:
        return False

    try:

        return (
            position.amount > 0
        )

    except Exception:

        return False


def get_position_amount(
    context,
    symbol
):
    """
    Get position quantity.

    Returns
    -------
    int
    """

    position = get_position(
        context,
        symbol
    )

    if position is None:
        return 0

    try:

        return int(
            position.amount
        )

    except Exception:

        return 0


def get_available_amount(
    context,
    symbol
):
    """
    Get sellable quantity.

    Returns
    -------
    int
    """

    position = get_position(
        context,
        symbol
    )

    if position is None:
        return 0

    try:

        return int(
            position.enable_amount
        )

    except Exception:

        return 0


def get_position_cost(
    context,
    symbol
):
    """
    Get average cost price.

    Returns
    -------
    float
    """

    position = get_position(
        context,
        symbol
    )

    if position is None:
        return 0.0

    try:

        return float(
            position.cost_basis
        )

    except Exception:

        return 0.0


def get_position_price(
    context,
    symbol
):
    """
    Get latest market price.

    Returns
    -------
    float
    """

    position = get_position(
        context,
        symbol
    )

    if position is None:
        return 0.0

    try:

        return float(
            position.last_sale_price
        )

    except Exception:

        return 0.0


def get_position_market_value(
    context,
    symbol
):
    """
    Get position market value.

    Returns
    -------
    float
    """

    amount = get_position_amount(
        context,
        symbol
    )

    price = get_position_price(
        context,
        symbol
    )

    return amount * price

# FIX-001C：统一 DATA-004 API
def get_equity(context):
    """
    Standard account equity API.
    """

    return get_total_equity(context)


def get_cash(context):
    """
    Standard account cash API.
    """

    return get_available_cash(context)


def validate_portfolio_access_layer(
    context
):
    """
    DATA-004 self validation.
    """

    equity = get_total_equity(
        context
    )

    cash = get_available_cash(
        context
    )

    positions = get_positions(
        context
    )

    assert isinstance(
        equity,
        float
    )

    assert isinstance(
        cash,
        float
    )

    assert isinstance(
        positions,
        dict
    )

    return True

# =========================================================
# IND-001
# Return Calculation
# =========================================================

RETURN_WINDOWS = {
    20,
    60,
    120,
    250,
}


def calc_return(
    symbol,
    lookback,
):
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

        raise ValueError(
            f"Unsupported lookback: {lookback}"
        )

    close = get_close(
        symbol,
        lookback + 1,
    )

    if len(close) < lookback + 1:

        return None

    start_price = close[0]
    end_price = close[-1]

    if start_price <= 0:

        return None

    return (
        end_price / start_price
        - 1.0
    )


# ---------------------------------------------------------
# Convenience Wrappers
# ---------------------------------------------------------

def return_20(symbol):

    return calc_return(
        symbol,
        20,
    )


def return_60(symbol):

    return calc_return(
        symbol,
        60,
    )


def return_120(symbol):

    return calc_return(
        symbol,
        120,
    )


def return_250(symbol):

    return calc_return(
        symbol,
        250,
    )

# =========================================================
# IND-001 Self Test
# =========================================================

def _test_return_calculation():

    sample_symbol = ETF_UNIVERSE[0]

    r20 = return_20(sample_symbol)
    r60 = return_60(sample_symbol)
    r120 = return_120(sample_symbol)
    r250 = return_250(sample_symbol)

    if r20 is not None:
        assert isinstance(r20, float)

    if r60 is not None:
        assert isinstance(r60, float)

    if r120 is not None:
        assert isinstance(r120, float)

    if r250 is not None:
        assert isinstance(r250, float)

    return True

# =========================================================
# IND-002
# Volatility Calculation
# =========================================================

import math


def calc_volatility(symbol, lookback=60):

    close = get_close(symbol, lookback + 1)

    if len(close) < lookback + 1:
        return None

    returns = []

    for i in range(1, len(close)):

        returns.append(
            close[i] / close[i - 1] - 1.0
        )

    mean_return = (
        sum(returns) / len(returns)
    )

    variance = sum(
        (r - mean_return) ** 2
        for r in returns
    ) / (len(returns) - 1)

    return (
        math.sqrt(variance)
        * math.sqrt(252)
    )

# =========================================================
# IND-002 Self Test
# =========================================================

def _test_volatility():

    sample_symbol = ETF_UNIVERSE[0]

    vol = calc_volatility(
        sample_symbol
    )

    if vol is not None:

        assert isinstance(
            vol,
            float
        )

        assert vol >= 0

    return True

# =========================================================
# IND-003
# Momentum Score
# =========================================================

MOMENTUM_WEIGHTS = {
    20: 0.05,
    60: 0.15,
    120: 0.30,
    250: 0.50,
}


def _percentile_rank(
    value,
    values,
):
    """
    Cross-sectional percentile rank.

    Returns
    -------
    float
        0 ~ 1
    """

    if value is None:
        return None

    valid_values = [
        v
        for v in values
        if v is not None
    ]

    if len(valid_values) <= 1:
        return 0.5

    valid_values.sort()

    rank = sum(
        1
        for v in valid_values
        if v <= value
    )

    return (
        rank - 1
    ) / (
        len(valid_values) - 1
    )


def calc_risk_adjusted_momentum(
    symbol,
    lookback,
):
    """
    Return / Volatility
    """

    ret = calc_return(
        symbol,
        lookback,
    )

    vol = calc_volatility(
        symbol,
        60,
    )

    if ret is None:
        return None

    if vol is None:
        return None

    if vol <= 0:
        return None

    return ret / vol


def calc_momentum_score(
    symbol,
):
    """
    Final momentum score.

    Returns
    -------
    float
        0 ~ 1
    """

    total_score = 0.0

    for lookback in RETURN_LOOKBACKS:

        cross_section = []

        for etf in RISK_ETFS:

            cross_section.append(
                calc_risk_adjusted_momentum(
                    etf,
                    lookback,
                )
            )

        raw_value = (
            calc_risk_adjusted_momentum(
                symbol,
                lookback,
            )
        )

        percentile = _percentile_rank(
            raw_value,
            cross_section,
        )

        if percentile is None:
            return None

        total_score += (
            MOMENTUM_WEIGHTS[lookback]
            * percentile
        )

    return total_score

# =========================================================
# IND-003 Self Test
# =========================================================

def _test_momentum_score():

    sample_symbol = ETF_UNIVERSE[0]

    score = calc_momentum_score(
        sample_symbol
    )

    if score is not None:

        assert isinstance(
            score,
            float
        )

        assert 0 <= score <= 1

    return True

# =========================================================
# IND-004
# Trend Quality Score
# =========================================================

QUALITY_LOOKBACK = 120


def calc_trend_quality_raw(
    symbol,
    lookback=QUALITY_LOOKBACK,
):
    """
    Raw trend quality.

    Quality =
    Slope × R²

    Uses log-price regression.

    Returns
    -------
    float
    """

    close = get_close(
        symbol,
        lookback,
    )

    if len(close) < lookback:

        return None

    if min(close) <= 0:

        return None

    log_prices = [
        math.log(price)
        for price in close
    ]

    x = list(
        range(len(log_prices))
    )

    n = len(x)

    x_mean = sum(x) / n
    y_mean = sum(log_prices) / n

    numerator = sum(
        (x[i] - x_mean)
        * (log_prices[i] - y_mean)
        for i in range(n)
    )

    denominator = sum(
        (x[i] - x_mean) ** 2
        for i in range(n)
    )

    if denominator == 0:

        return None

    slope = (
        numerator
        / denominator
    )

    fitted = [
        y_mean
        + slope * (xi - x_mean)
        for xi in x
    ]

    ss_total = sum(
        (y - y_mean) ** 2
        for y in log_prices
    )

    if ss_total <= 0:

        return None

    ss_residual = sum(
        (
            log_prices[i]
            - fitted[i]
        ) ** 2
        for i in range(n)
    )

    r_squared = (
        1.0
        - ss_residual / ss_total
    )

    return (
        slope
        * r_squared
    )


def calc_quality_score(
    symbol,
):
    """
    Cross-sectional quality score.

    Returns
    -------
    float
        0 ~ 1
    """

    raw_values = []

    for etf in RISK_ETFS:

        raw_values.append(
            calc_trend_quality_raw(
                etf
            )
        )

    raw_value = (
        calc_trend_quality_raw(
            symbol
        )
    )

    return _percentile_rank(
        raw_value,
        raw_values,
    )

# =========================================================
# IND-004 Self Test
# =========================================================

def _test_quality_score():

    sample_symbol = ETF_UNIVERSE[0]

    score = calc_quality_score(
        sample_symbol
    )

    if score is not None:

        assert isinstance(
            score,
            float
        )

        assert 0 <= score <= 1

    return True

# =========================================================
# IND-005
# Liquidity Score
# =========================================================

LIQUIDITY_LOOKBACK = 60

def calc_adv60(
    symbol,
    lookback=LIQUIDITY_LOOKBACK,
):
    """
    Average Daily Turnover.

    Returns
    -------
    float
    """

    turnover = get_turnover(
        symbol,
        lookback,
    )

    if turnover is None:
        return None

    if len(turnover) < lookback:
        return None

    return (
        sum(turnover)
        / len(turnover)
    )

def calc_liquidity_score(
    symbol,
):
    """
    Cross-sectional liquidity score.

    Returns
    -------
    float
        0 ~ 1
    """

    cross_section = []

    for etf in RISK_ETFS:

        cross_section.append(
            calc_adv60(etf)
        )

    raw_value = calc_adv60(
        symbol
    )

    return _percentile_rank(
        raw_value,
        cross_section,
    )

# =========================================================
# IND-005 Self Test
# =========================================================

def _test_liquidity_score():

    sample_symbol = ETF_UNIVERSE[0]

    score = calc_liquidity_score(
        sample_symbol
    )

    if score is not None:

        assert isinstance(
            score,
            float
        )

        assert 0 <= score <= 1

    return True

# =========================================================
# IND-006
# ATR20
# =========================================================

ATR_LOOKBACK = 20

def calc_true_range(
    high,
    low,
    prev_close,
):
    """
    True Range.

    Returns
    -------
    float
    """

    return max(
        high - low,
        abs(high - prev_close),
        abs(low - prev_close),
    )

def calc_atr(
    symbol,
    lookback=ATR_LOOKBACK,
):
    """
    ATR20.

    Returns
    -------
    float
    """

    high = get_high(
        symbol,
        lookback + 1,
    )

    low = get_low(
        symbol,
        lookback + 1,
    )

    close = get_close(
        symbol,
        lookback + 1,
    )

    if (
        len(high) < lookback + 1
        or len(low) < lookback + 1
        or len(close) < lookback + 1
    ):
        return None

    tr_values = []

    for i in range(1, len(close)):

        tr = calc_true_range(
            high[i],
            low[i],
            close[i - 1],
        )

        tr_values.append(tr)

    if len(tr_values) == 0:

        return None

    return (
        sum(tr_values)
        / len(tr_values)
    )

def calc_atr_percent(
    symbol,
):
    """
    ATR as percentage of price.

    Returns
    -------
    float
    """

    atr = calc_atr(
        symbol
    )

    close = get_close(
        symbol,
        1,
    )

    if atr is None:

        return None

    if len(close) == 0:

        return None

    if close[-1] <= 0:

        return None

    return (
        atr
        / close[-1]
    )

# =========================================================
# IND-006 Self Test
# =========================================================

def _test_atr():

    sample_symbol = ETF_UNIVERSE[0]

    atr = calc_atr(
        sample_symbol
    )

    if atr is not None:

        assert atr >= 0

    atr_pct = calc_atr_percent(
        sample_symbol
    )

    if atr_pct is not None:

        assert atr_pct >= 0

    return True

# =========================================================
# FILTER-001
# Market Breadth
# =========================================================

MARKET_FILTER_INDEXES = (
    "510300",  # CSI300
    "510500",  # CSI500
    "512100",  # CSI1000
)

MA_SHORT = 50
MA_MID = 150
MA_LONG = 250

def calc_ma(
    symbol,
    period,
):
    """
    Simple moving average.
    """

    close = get_close(
        symbol,
        period,
    )

    if len(close) < period:

        return None

    return (
        sum(close[-period:])
        / float(period)
    )

def is_bull_trend(
    symbol,
):
    """
    Close > MA50 > MA150 > MA250
    """

    close = get_close(
        symbol,
        MA_LONG,
    )

    if len(close) < MA_LONG:

        return False

    latest_close = close[-1]

    ma50 = calc_ma(
        symbol,
        MA_SHORT,
    )

    ma150 = calc_ma(
        symbol,
        MA_MID,
    )

    ma250 = calc_ma(
        symbol,
        MA_LONG,
    )

    if (
        ma50 is None
        or ma150 is None
        or ma250 is None
    ):
        return False

    return (
        latest_close > ma50
        and ma50 > ma150
        and ma150 > ma250
    )

def calc_market_score():
    """
    Market breadth score.

    Returns
    -------
    int
        0 ~ 3
    """

    score = 0

    for symbol in MARKET_FILTER_INDEXES:

        if is_bull_trend(symbol):

            score += 1

    return score

# =========================================================
# FILTER-001 Self Test
# =========================================================

def _test_market_score():

    score = calc_market_score()

    assert isinstance(
        score,
        int,
    )

    assert 0 <= score <= 3

    print(
        "FILTER-001 validation passed."
    )

# =========================================================
# FILTER-002
# Market Exposure
# =========================================================

MARKET_EXPOSURE_MAP = {
    0: 0.00,
    1: 0.50,
    2: 0.80,
    3: 1.00,
}

def calc_market_exposure():
    """
    Convert market score
    into portfolio exposure.
    """

    score = calc_market_score()

    return MARKET_EXPOSURE_MAP.get(
        score,
        0.0,
    )

# =========================================================
# FILTER-002 Self Test
# =========================================================

def _test_market_exposure():

    exposure = calc_market_exposure()

    assert isinstance(
        exposure,
        float,
    )

    assert (
        0.0
        <= exposure
        <= 1.0
    )

    print(
        "FILTER-002 validation passed."
    )

# =========================================================
# RANK-001
# Final Score
# =========================================================

MOMENTUM_SCORE_WEIGHT = 0.70
QUALITY_SCORE_WEIGHT = 0.20
LIQUIDITY_SCORE_WEIGHT = 0.10

def calc_final_score(
    symbol,
):
    """
    Final ETF ranking score.

    Returns
    -------
    float
        0 ~ 1
    """

    momentum_score = (
        calc_momentum_score(
            symbol
        )
    )

    quality_score = (
        calc_quality_score(
            symbol
        )
    )

    liquidity_score = (
        calc_liquidity_score(
            symbol
        )
    )

    if (
        momentum_score is None
        or quality_score is None
        or liquidity_score is None
    ):
        return None

    return (
        MOMENTUM_SCORE_WEIGHT
        * momentum_score
        + QUALITY_SCORE_WEIGHT
        * quality_score
        + LIQUIDITY_SCORE_WEIGHT
        * liquidity_score
    )

def get_ranked_etfs():
    """
    Return ETFs sorted by final score.
    """

    scores = []

    for symbol in RISK_ETFS:

        score = calc_final_score(
            symbol
        )

        if score is None:
            continue

        scores.append(
            (
                symbol,
                score,
            )
        )

    scores.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    return scores

# =========================================================
# RANK-001 Self Test
# =========================================================

def _test_final_score():

    sample_symbol = RISK_ETFS[0]

    score = calc_final_score(
        sample_symbol
    )

    if score is not None:

        assert isinstance(
            score,
            float,
        )

        assert (
            0.0
            <= score
            <= 1.0
        )

    print(
        "RANK-001 validation passed."
    )

    return True

def _test_ranked_etfs():

    ranked = get_ranked_etfs()

    if len(ranked) > 1:

        for i in range(
            len(ranked) - 1
        ):

            assert (
                ranked[i][1]
                >= ranked[i + 1][1]
            )

    return True

# =========================================================
# RANK-002
# ETF Selection
# =========================================================

MAX_PORTFOLIO_SIZE = 5

RANKING_TREND_MA = 200

def passes_ranking_filter(
    symbol,
):
    """
    ETF trend filter.

    Close > MA200
    """

    close = get_close(
        symbol,
        RANKING_TREND_MA,
    )

    if len(close) < RANKING_TREND_MA:

        return False

    ma200 = calc_ma(
        symbol,
        RANKING_TREND_MA,
    )

    if ma200 is None:

        return False

    return close[-1] > ma200

def get_selected_etfs():
    """
    Select final ETF portfolio.
    """

    candidates = []

    for symbol in RISK_ETFS:

        if not passes_ranking_filter(
            symbol
        ):
            continue

        score = calc_final_score(
            symbol
        )

        if score is None:
            continue

        candidates.append(
            (
                symbol,
                score,
            )
        )

    candidates.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        symbol
        for symbol, score
        in candidates[
            :MAX_PORTFOLIO_SIZE
        ]
    ]

def get_selected_etfs_with_score():

    candidates = []

    for symbol in RISK_ETFS:

        if not passes_ranking_filter(
            symbol
        ):
            continue

        score = calc_final_score(
            symbol
        )

        if score is None:
            continue

        candidates.append(
            (
                symbol,
                score,
            )
        )

    candidates.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    return candidates[
        :MAX_PORTFOLIO_SIZE
    ]

# =========================================================
# RANK-002 Self Test
# =========================================================

def _test_selected_etfs():

    selected = get_selected_etfs()

    assert isinstance(
        selected,
        list,
    )

    assert (
        len(selected)
        <= MAX_PORTFOLIO_SIZE
    )

    print(
        "RANK-002 validation passed."
    )

    return True

def validate_ranking_pipeline():
    """
    Validate ranking pipeline.
    """

    ranked = get_ranked_etfs()

    assert ranked is not None

    assert len(ranked) > 0

    previous_score = 999

    for symbol, score in ranked:

        assert score is not None

        assert 0.0 <= score <= 1.0

        assert score <= previous_score

        previous_score = score

    selected = get_selected_etfs()

    assert selected is not None

    assert len(selected) <= MAX_PORTFOLIO_SIZE

    return True

# =========================================================
# PORT-001
# Position Sizing
# =========================================================

def calc_inverse_volatility_weights(
    symbols,
):
    """
    Calculate inverse ATR weights.

    Parameters
    ----------
    symbols : list[str]

    Returns
    -------
    dict
        symbol -> raw weight
    """

    risk_values = {}

    for symbol in symbols:

        atr_pct = calc_atr_percent(
            symbol
        )

        if atr_pct is None:
            continue

        if atr_pct <= 0:
            continue

        risk_values[symbol] = (
            1.0 / atr_pct
        )

    if len(risk_values) == 0:

        return {}

    total_risk = sum(
        risk_values.values()
    )

    return {
        symbol: value / total_risk
        for symbol, value
        in risk_values.items()
    }

def calc_weights():
    """
    Calculate portfolio target weights.

    Returns
    -------
    dict
        symbol -> weight
    """

    selected = get_selected_etfs()

    if len(selected) == 0:

        return {}

    return calc_inverse_volatility_weights(
        selected
    )

# =========================================================
# PORT-001 Self Test
# =========================================================

def _test_position_sizing():

    weights = calc_weights()

    if len(weights) == 0:

        return True

    total_weight = sum(
        weights.values()
    )

    assert abs(
        total_weight - 1.0
    ) < 0.0001

    for weight in weights.values():

        assert weight > 0

    print(
        "PORT-001 validation passed."
    )

    return True


# =========================================================
# PORT-002
# Portfolio Constraints
# =========================================================

# Portfolio Constraints
MAX_SINGLE_POSITION_WEIGHT = 0.25
MIN_SINGLE_POSITION_WEIGHT = 0.05

def normalize_weights(
    weights,
):
    """
    Normalize weights to 100%.
    """

    if len(weights) == 0:
        return {}

    total = sum(
        weights.values()
    )

    if total <= 0:
        return {}

    return {
        symbol: weight / total
        for symbol, weight
        in weights.items()
    }

def apply_max_position_constraint(
    weights,
):
    """
    Apply maximum position limit.
    """

    adjusted = {}

    excess = 0.0

    for symbol, weight in weights.items():

        if weight > MAX_SINGLE_POSITION_WEIGHT:

            excess += (
                weight -
                MAX_SINGLE_POSITION_WEIGHT
            )

            adjusted[symbol] = (
                MAX_SINGLE_POSITION_WEIGHT
            )

        else:

            adjusted[symbol] = weight

    if excess <= 0:

        return adjusted

    eligible = [
        s
        for s, w
        in adjusted.items()
        if w < MAX_SINGLE_POSITION_WEIGHT
    ]

    if len(eligible) == 0:

        return adjusted

    redistribution = (
        excess / len(eligible)
    )

    for symbol in eligible:

        adjusted[symbol] += (
            redistribution
        )

    return adjusted

def apply_min_position_constraint(
    weights,
):
    """
    Remove positions below minimum size.
    """

    adjusted = {}

    for symbol, weight in weights.items():

        if (
            weight >=
            MIN_SINGLE_POSITION_WEIGHT
        ):

            adjusted[symbol] = weight

    return adjusted

def calc_target_weights():
    """
    Final portfolio weights.
    """

    weights = calc_weights()

    if len(weights) == 0:

        return {}

    weights = apply_max_position_constraint(
        weights
    )

    weights = normalize_weights(
        weights
    )

    weights = apply_min_position_constraint(
        weights
    )

    weights = normalize_weights(
        weights
    )

    return weights

# =========================================================
# PORT-002 Self Test
# =========================================================

def _test_portfolio_constraints():

    weights = calc_target_weights()

    if len(weights) == 0:

        return True

    total = sum(
        weights.values()
    )

    assert abs(
        total - 1.0
    ) < 0.0001

    for weight in weights.values():

        assert (
            weight <=
            MAX_SINGLE_POSITION_WEIGHT + 0.01
        )

        assert (
            weight >=
            MIN_SINGLE_POSITION_WEIGHT
        )

    print(
        "PORT-002 validation passed."
    )

    return True

# =========================================================
# RISK-001
# Portfolio Risk Engine
# =========================================================

def calc_portfolio_atr():

    weights = calc_target_weights()

    if len(weights) == 0:

        return None

    total_risk = 0.0

    total_weight = 0.0

    for symbol, weight in weights.items():

        atr_pct = calc_atr_percent(
            symbol
        )

        if atr_pct is None:
            continue

        total_risk += (
            atr_pct * weight
        )

        total_weight += weight

    if total_weight <= 0:

        return None

    return (
        total_risk /
        total_weight
    ) 

def calc_portfolio_volatility():

    weights = calc_target_weights()

    if len(weights) == 0:

        return None

    total_vol = 0.0

    total_weight = 0.0

    for symbol, weight in weights.items():

        vol = calc_volatility(
            symbol
        )

        if vol is None:
            continue

        total_vol += (
            vol * weight
        )

        total_weight += weight

    if total_weight <= 0:

        return None

    return (
        total_vol /
        total_weight
    )

def get_portfolio_statistics():

    weights = calc_target_weights()

    return {

        "position_count":
            len(weights),

        "portfolio_atr":
            calc_portfolio_atr(),

        "portfolio_volatility":
            calc_portfolio_volatility(),
    }

def calc_risk_budget_usage():

    stats = (
        get_portfolio_statistics()
    )

    portfolio_vol = stats.get(
        "portfolio_volatility"
    )

    if portfolio_vol is None:

        return None

    if TARGET_PORTFOLIO_RISK <= 0:

        return None

    return (
        portfolio_vol /
        TARGET_PORTFOLIO_RISK
    )

def get_risk_state():

    usage = (
        calc_risk_budget_usage()
    )

    if usage is None:

        return "UNKNOWN"

    if usage < 0.8:

        return "LOW"

    if usage < 1.0:

        return "NORMAL"

    return "HIGH"

# =========================================================
# RISK-001 Self Test
# =========================================================

def _test_risk_engine():

    stats = (
        get_portfolio_statistics()
    )

    assert isinstance(
        stats,
        dict
    )

    assert (
        "position_count"
        in stats
    )

    assert (
        "portfolio_atr"
        in stats
    )

    assert (
        "portfolio_volatility"
        in stats
    )

    print(
        "RISK-001 validation passed."
    )

    return True

# =========================================================
# Self Test
# =========================================================

if __name__ == "__main__":
    validate_universe()
    print("DATA-001 validation passed.")

    validate_config()
    print("DATA-002 validation passed.")

    _test_logging()
    print("FIX-001B: 增加日志接口 Logging passed")

    _test_state_management()
    print("STATE-001 validation passed.")

    # _test_data_layer()
    # print("DATA-003 validation passed.")
    print(
        "DATA-003 validation skipped "
        "(requires PTrade runtime)."
    )

    # validate_portfolio_access_layer(context)
    # print("DATA-004 validation passed.")
    print(
        "DATA-004 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_return_calculation()
    # print("IND-001 validation passed.")
    print(
        "IND-001 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_volatility()
    # print("IND-002 validation passed.")

    print(
        "IND-002 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_momentum_score()
    # print("IND-003 validation passed.")

    print(
        "IND-003 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_quality_score()
    # print("IND-004 validation passed.")

    print(
        "IND-004 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_liquidity_score()
    # print("IND-005 validation passed.")

    print(
        "IND-005 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_atr()
    # print("IND-006 validation passed.")

    print(
        "IND-006 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_market_score()
    print(
        "FILTER-001 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_market_exposure()
    print(
        "FILTER-002 validation skipped "
        "(requires PTrade runtime)."
    )

    # _test_final_score()
    # _test_ranked_etfs()
    print(
        "RANK-001 validation skipped "
        "(requires PTrade runtime)."
    )   

    # _test_selected_etfs()
    # if validate_ranking_pipeline():
    #     print("RANK validation passed.")
    print(
        "RANK-002 validation skipped "
        "(requires PTrade runtime)."
    )   

    # _test_position_sizing()
    print(
        "PORT-001 validation skipped "
        "(requires PTrade runtime)."
    )   

    # _test_position_sizing()
    # _test_portfolio_constraints()
    print(
        "PORT-002 validation skipped "
        "(requires PTrade runtime)."
    )   

    # _test_risk_engine()
    print(
        "RISK-001 validation skipped "
        "(requires PTrade runtime)."
    )   