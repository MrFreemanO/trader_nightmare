"""
Production-ready logging configuration for trading bot
"""

import logging
import logging.handlers
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
            "thread": record.thread,
            "process": record.process,
        }
        
        # Add extra fields if present
        if hasattr(record, 'trade_id'):
            log_entry['trade_id'] = record.trade_id
        if hasattr(record, 'token_address'):
            log_entry['token_address'] = record.token_address
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'execution_time'):
            log_entry['execution_time'] = record.execution_time
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info) if record.exc_info else None
            }
        
        return json.dumps(log_entry, ensure_ascii=False)

class TradingLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter for adding trading-specific context"""
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Add extra context to log messages"""
        extra = kwargs.get('extra', {})
        
        # Add context from adapter
        if self.extra:
            extra.update(self.extra)
        
        kwargs['extra'] = extra
        return msg, kwargs

def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "/var/log/trading-bot",
    enable_json: bool = True,
    enable_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """
    Setup comprehensive logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        enable_json: Enable JSON formatted logging
        enable_console: Enable console logging
        max_file_size: Maximum size of log files before rotation
        backup_count: Number of backup files to keep
    """
    
    # Create log directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        if enable_json:
            console_handler.setFormatter(JSONFormatter())
        else:
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
        
        root_logger.addHandler(console_handler)
    
    # File handlers
    handlers_config = [
        {
            "filename": os.path.join(log_dir, "app.log"),
            "level": logging.INFO,
            "formatter": "standard" if not enable_json else "json"
        },
        {
            "filename": os.path.join(log_dir, "error.log"),
            "level": logging.ERROR,
            "formatter": "standard" if not enable_json else "json"
        },
        {
            "filename": os.path.join(log_dir, "trading.log"),
            "level": logging.INFO,
            "formatter": "json",
            "filter": "trading"
        },
        {
            "filename": os.path.join(log_dir, "performance.log"),
            "level": logging.INFO,
            "formatter": "json",
            "filter": "performance"
        }
    ]
    
    for handler_config in handlers_config:
        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=handler_config["filename"],
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(handler_config["level"])
        
        # Set formatter
        if handler_config["formatter"] == "json":
            file_handler.setFormatter(JSONFormatter())
        else:
            standard_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(standard_formatter)
        
        # Add filter if specified
        if "filter" in handler_config:
            filter_name = handler_config["filter"]
            if filter_name == "trading":
                file_handler.addFilter(TradingLogFilter())
            elif filter_name == "performance":
                file_handler.addFilter(PerformanceLogFilter())
        
        root_logger.addHandler(file_handler)
    
    # Configure specific loggers
    configure_specific_loggers()
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized", extra={
        "log_level": log_level,
        "log_dir": log_dir,
        "json_enabled": enable_json
    })

class TradingLogFilter(logging.Filter):
    """Filter for trading-related log messages"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter trading-related messages"""
        trading_keywords = [
            'trade', 'position', 'signal', 'viability', 'execution',
            'pnl', 'profit', 'loss', 'buy', 'sell', 'token'
        ]
        
        message = record.getMessage().lower()
        return any(keyword in message for keyword in trading_keywords)

class PerformanceLogFilter(logging.Filter):
    """Filter for performance-related log messages"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter performance-related messages"""
        performance_keywords = [
            'performance', 'latency', 'response_time', 'execution_time',
            'memory', 'cpu', 'cache', 'database', 'api_call'
        ]
        
        message = record.getMessage().lower()
        return any(keyword in message for keyword in performance_keywords) or hasattr(record, 'execution_time')

def configure_specific_loggers():
    """Configure specific loggers for different components"""
    
    # Reduce verbosity of external libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    # Set appropriate levels for application components
    logging.getLogger('trading_bot.scout').setLevel(logging.INFO)
    logging.getLogger('trading_bot.executor').setLevel(logging.INFO)
    logging.getLogger('trading_bot.exit').setLevel(logging.INFO)
    logging.getLogger('trading_bot.data').setLevel(logging.INFO)
    logging.getLogger('trading_bot.api').setLevel(logging.INFO)

def get_logger(name: str, **context) -> TradingLoggerAdapter:
    """
    Get a logger with trading-specific context
    
    Args:
        name: Logger name
        **context: Additional context to include in all log messages
    
    Returns:
        TradingLoggerAdapter instance
    """
    logger = logging.getLogger(name)
    return TradingLoggerAdapter(logger, context)

def log_performance(func):
    """Decorator to log function performance"""
    import time
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(f"performance.{func.__module__}.{func.__name__}")
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.info(
                f"Function {func.__name__} completed successfully",
                extra={
                    "execution_time": execution_time,
                    "function": func.__name__,
                    "module": func.__module__,
                    "success": True
                }
            )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            logger.error(
                f"Function {func.__name__} failed",
                extra={
                    "execution_time": execution_time,
                    "function": func.__name__,
                    "module": func.__module__,
                    "success": False,
                    "error": str(e)
                },
                exc_info=True
            )
            
            raise
    
    return wrapper

def log_trade_event(event_type: str, **details):
    """Log trading events with structured data"""
    logger = get_logger("trading_bot.events")
    
    log_data = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        **details
    }
    
    logger.info(f"Trading event: {event_type}", extra=log_data)

# Example usage functions
def log_trade_execution(trade_id: str, token_address: str, action: str, price: float, amount: float):
    """Log trade execution event"""
    log_trade_event(
        "trade_execution",
        trade_id=trade_id,
        token_address=token_address,
        action=action,
        price=price,
        amount=amount
    )

def log_signal_generation(token_address: str, signal_type: str, confidence: float, viability_score: float):
    """Log signal generation event"""
    log_trade_event(
        "signal_generation",
        token_address=token_address,
        signal_type=signal_type,
        confidence=confidence,
        viability_score=viability_score
    )

def log_position_update(position_id: str, token_address: str, pnl: float, status: str):
    """Log position update event"""
    log_trade_event(
        "position_update",
        position_id=position_id,
        token_address=token_address,
        pnl=pnl,
        status=status
    )

# Initialize logging if this module is imported
if __name__ != "__main__":
    # Get configuration from environment variables
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_dir = os.getenv("LOG_DIR", "/var/log/trading-bot")
    enable_json = os.getenv("LOG_JSON", "true").lower() == "true"
    
    # Create log directory if running in development
    if not os.path.exists(log_dir):
        log_dir = "./logs"
        Path(log_dir).mkdir(exist_ok=True)
    
    setup_logging(
        log_level=log_level,
        log_dir=log_dir,
        enable_json=enable_json
    )

