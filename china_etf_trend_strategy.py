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

# =========================================================
# Self Test
# =========================================================

if __name__ == "__main__":
    validate_universe()
    print("DATA-001 validation passed.")