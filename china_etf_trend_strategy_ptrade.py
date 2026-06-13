# =========================================================
# MIG-001A PTrade Lifecycle
# =========================================================

def initialize(context):
    log.info("MIG-001A initialize()")
    validate_ptrade_environment(context)
    
    g.MAX_LOOKBACK = 252
    
    run_daily(context, daily_heartbeat, time='14:50')

def before_trading_start(context, data):
    log.info("MIG-001A before_trading_start()")
    

def after_trading_end(context, data):
    log.info("MIG-001A after_trading_end()")
    
# =========================================================
# MIG-001B Environment Validation
# =========================================================

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
            
def daily_heartbeat(context):
    log.info("daily_heartbeat()")
    
    validate_data_interface()
    
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