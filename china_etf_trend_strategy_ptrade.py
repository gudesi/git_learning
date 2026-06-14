# =========================================================
# Strategy Configuration
# =========================================================


# Cash ETF

CASH_ETF = "511880"


# Broad Market ETFs

BROAD_ETFS = [
    "510300",  # CSI 300
    "510500",  # CSI 500
    "512100",  # CSI 1000
    "563300",  # CSI A500
    "159915",  # ChiNext
    "588000",  # STAR50
    "510880",  # Dividend
]


# Financial ETFs

FINANCIAL_ETFS = [
    "512880",  # Securities
    "512800",  # Banking
]


# Technology ETFs

TECH_ETFS = [
    "512480",  # Semiconductor
    "159819",  # AI
    "562500",  # Robotics
    "512980",  # Media
    "516160",  # New Energy
]


# Defense ETFs

DEFENSE_ETFS = [
    "512660",  # Military
]


# Healthcare ETFs

HEALTHCARE_ETFS = [
    "512010",  # Healthcare
]


# Consumer ETFs

CONSUMER_ETFS = [
    "159928",  # Consumer
]


# Resource ETFs

RESOURCE_ETFS = [
    "512400",  # Nonferrous Metals
    "518880",  # Gold
    "515220",  # Coal
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

RETURN_LOOKBACKS = (
    20,
    60,
    120,
    250,
)

ATR_LOOKBACK = 20


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
    
    validate_turnover_api()
    
def _get_history_field(symbol, field, count):
    try:
        
        data = get_history(count, '1d', field, symbol, fq=None, include=False)

        return data

    except Exception as e:

        log.error("_get_history_field failed: " + str(e))

        return None
        
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