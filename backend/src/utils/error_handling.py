"""
Error handling utilities for production-ready trading bot
"""

import logging
import time
import functools
from typing import Any, Callable, Dict, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class RetryConfig:
    """Configuration for retry logic"""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True

class CircuitBreaker:
    """Circuit breaker implementation for external service calls"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60, name: str = "default"):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.name = name
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED
        self.success_count = 0
        
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker {self.name} transitioning to HALF_OPEN")
            else:
                raise CircuitBreakerOpenError(f"Circuit breaker {self.name} is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        return datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout)
    
    def _on_success(self):
        """Handle successful call"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 3:  # Require 3 successes to fully close
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                logger.info(f"Circuit breaker {self.name} reset to CLOSED")
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker {self.name} opened after {self.failure_count} failures")

class CircuitBreakerOpenError(Exception):
    """Exception raised when circuit breaker is open"""
    pass

def with_retry(config: RetryConfig = None):
    """Decorator for adding retry logic to functions"""
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt == config.max_attempts - 1:
                        logger.error(f"Function {func.__name__} failed after {config.max_attempts} attempts: {e}")
                        break
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        config.base_delay * (config.exponential_base ** attempt),
                        config.max_delay
                    )
                    
                    # Add jitter to prevent thundering herd
                    if config.jitter:
                        import random
                        delay *= (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{config.max_attempts}), retrying in {delay:.2f}s: {e}")
                    time.sleep(delay)
            
            raise last_exception
        
        return wrapper
    return decorator

def handle_api_errors(func: Callable) -> Callable:
    """Decorator for robust API error handling"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            result = func(*args, **kwargs)
            return {"success": True, "data": result}
        except ConnectionError as e:
            logger.error(f"Connection error in {func.__name__}: {e}")
            return {"success": False, "error": "Connection failed", "retry": True, "error_type": "connection"}
        except TimeoutError as e:
            logger.error(f"Timeout error in {func.__name__}: {e}")
            return {"success": False, "error": "Request timeout", "retry": True, "error_type": "timeout"}
        except CircuitBreakerOpenError as e:
            logger.error(f"Circuit breaker open in {func.__name__}: {e}")
            return {"success": False, "error": "Service unavailable", "retry": False, "error_type": "circuit_breaker"}
        except ValueError as e:
            logger.error(f"Validation error in {func.__name__}: {e}")
            return {"success": False, "error": "Invalid data", "retry": False, "error_type": "validation"}
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            return {"success": False, "error": "Internal error", "retry": False, "error_type": "internal"}
    
    return wrapper

class ErrorTracker:
    """Track and analyze error patterns"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.errors = []
    
    def record_error(self, error_type: str, function_name: str, details: str = ""):
        """Record an error occurrence"""
        error_record = {
            "timestamp": datetime.now(),
            "error_type": error_type,
            "function_name": function_name,
            "details": details
        }
        
        self.errors.append(error_record)
        
        # Keep only recent errors
        if len(self.errors) > self.window_size:
            self.errors = self.errors[-self.window_size:]
    
    def get_error_rate(self, time_window: timedelta = timedelta(minutes=5)) -> float:
        """Calculate error rate within time window"""
        cutoff_time = datetime.now() - time_window
        recent_errors = [e for e in self.errors if e["timestamp"] > cutoff_time]
        
        if not recent_errors:
            return 0.0
        
        return len(recent_errors) / self.window_size
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of error patterns"""
        if not self.errors:
            return {"total_errors": 0, "error_types": {}, "functions": {}}
        
        error_types = {}
        functions = {}
        
        for error in self.errors:
            error_type = error["error_type"]
            function_name = error["function_name"]
            
            error_types[error_type] = error_types.get(error_type, 0) + 1
            functions[function_name] = functions.get(function_name, 0) + 1
        
        return {
            "total_errors": len(self.errors),
            "error_types": error_types,
            "functions": functions,
            "error_rate": self.get_error_rate()
        }

# Global error tracker instance
error_tracker = ErrorTracker()

def track_errors(func: Callable) -> Callable:
    """Decorator to track errors in the global error tracker"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_tracker.record_error(
                error_type=type(e).__name__,
                function_name=func.__name__,
                details=str(e)
            )
            raise
    
    return wrapper

# Circuit breaker instances for different services
circuit_breakers = {
    "coingecko": CircuitBreaker(failure_threshold=3, timeout=30, name="coingecko"),
    "bitquery": CircuitBreaker(failure_threshold=3, timeout=30, name="bitquery"),
    "dexscreener": CircuitBreaker(failure_threshold=3, timeout=30, name="dexscreener"),
    "database": CircuitBreaker(failure_threshold=5, timeout=60, name="database"),
}

def get_circuit_breaker(service_name: str) -> CircuitBreaker:
    """Get circuit breaker for a specific service"""
    return circuit_breakers.get(service_name, circuit_breakers["database"])

# Example usage functions
@handle_api_errors
@track_errors
def safe_api_call(service_name: str, api_function: Callable, *args, **kwargs):
    """Make a safe API call with circuit breaker protection"""
    circuit_breaker = get_circuit_breaker(service_name)
    return circuit_breaker.call(api_function, *args, **kwargs)

@with_retry(RetryConfig(max_attempts=3, base_delay=1.0))
@handle_api_errors
@track_errors
def resilient_database_operation(operation: Callable, *args, **kwargs):
    """Execute database operation with retry and error handling"""
    circuit_breaker = get_circuit_breaker("database")
    return circuit_breaker.call(operation, *args, **kwargs)

