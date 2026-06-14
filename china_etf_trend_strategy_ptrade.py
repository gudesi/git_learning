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
    
    validate_portfolio_snapshot(context)
    
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