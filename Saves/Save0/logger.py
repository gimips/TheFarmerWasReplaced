# --- Logging Configuration ---
DEBUG = 10
INFO = 20
WARN = 30
ERROR = 40
CRITICAL = 50

log_threshold = INFO

def set_level(level):
    global log_threshold
    log_threshold = level

def log_msg(level, label, message):
    if level >= log_threshold:
        time = get_time()
        tick = get_tick_count()
        formatted_msg = '[' + label + '] T:' + str(time) + ' | K:' + str(tick) + ' | ' + str(message)
        quick_print(formatted_msg)

def debug(message):
    log_msg(10, 'DEBUG', message)

def info(message):
    log_msg(20, 'INFO', message)

def warning(message):
    log_msg(30, 'WARN', message)

def error(message):
    log_msg(40, 'ERROR', message)

def critical(message):
    log_msg(50, 'CRITICAL', message)