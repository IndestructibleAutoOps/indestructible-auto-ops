#!/usr/bin/env python3
"""
Enhanced Logging Module for Production Bug Investigation
Provides structured, context-aware logging with performance tracking
"""

import logging
import sys
import time
import traceback
from functools import wraps
from contextlib import contextmanager
from typing import Any, Dict, Optional
import json
import os

# Log levels
TRACE = 5
logging.addLevelName(TRACE, "TRACE")

class StructuredLogger:
    """Enhanced logger with structured output and context"""
    
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # File handler for persistent logs
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(
            os.path.join(log_dir, f"{name}.log")
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        # Context storage
        self.context: Dict[str, Any] = {}
    
    def add_context(self, **kwargs):
        """Add contextual information to logs"""
        self.context.update(kwargs)
    
    def clear_context(self):
        """Clear all context"""
        self.context.clear()
    
    def _format_message(self, message: str, **kwargs) -> str:
        """Format message with context and extra data"""
        combined = {**self.context, **kwargs}
        if combined:
            return f"{message} | Context: {json.dumps(combined)}"
        return message
    
    def trace(self, message: str, **kwargs):
        """Log at TRACE level"""
        self.logger.log(TRACE, self._format_message(message, **kwargs))
    
    def debug(self, message: str, **kwargs):
        """Log at DEBUG level"""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """Log at INFO level"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log at WARNING level"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log at ERROR level with exception details"""
        if exception:
            kwargs['exception_type'] = type(exception).__name__
            kwargs['exception_message'] = str(exception)
            kwargs['traceback'] = traceback.format_exc()
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log at CRITICAL level with full details"""
        if exception:
            kwargs['exception_type'] = type(exception).__name__
            kwargs['exception_message'] = str(exception)
            kwargs['traceback'] = traceback.format_exc()
        self.logger.critical(self._format_message(message, **kwargs))

# Performance tracking decorator
def log_performance(logger: StructuredLogger):
    """Decorator to log function execution time"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            function_name = func.__name__
            
            logger.debug(f"Starting {function_name}", 
                        args=str(args)[:100], 
                        kwargs=str(kwargs)[:100])
            
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                logger.info(f"Completed {function_name}", 
                           elapsed_seconds=round(elapsed_time, 3))
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                logger.error(f"Failed {function_name}", 
                            exception=e,
                            elapsed_seconds=round(elapsed_time, 3))
                raise
        return wrapper
    return decorator

# Context manager for operation logging
@contextmanager
def log_operation(logger: StructuredLogger, operation_name: str, **context):
    """Context manager for logging operation lifecycle"""
    logger.info(f"Starting operation: {operation_name}", **context)
    start_time = time.time()
    
    try:
        yield
        elapsed_time = time.time() - start_time
        logger.info(f"Operation completed: {operation_name}", 
                   elapsed_seconds=round(elapsed_time, 3))
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(f"Operation failed: {operation_name}", 
                    exception=e,
                    elapsed_seconds=round(elapsed_time, 3))
        raise

# Retry mechanism with logging
def retry_with_backoff(
    logger: StructuredLogger,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0
):
    """Decorator for retrying failed operations with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}",
                                    exception=e)
                        raise
                    
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    logger.warning(f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}. "
                                 f"Retrying in {delay:.1f}s...",
                                 error_type=type(e).__name__,
                                 error_message=str(e),
                                 attempt=attempt + 1,
                                 next_retry_delay=delay)
                    time.sleep(delay)
        return wrapper
    return decorator

# Example usage
if __name__ == "__main__":
    logger = StructuredLogger("bug_investigation", level=logging.DEBUG)
    
    # Test logging
    logger.info("Application started", version="1.0.0", environment="development")
    
    # Test performance logging
    @log_performance(logger)
    def test_function(x):
        time.sleep(0.1)
        return x * 2
    
    result = test_function(5)
    logger.info(f"Result: {result}")
    
    # Test operation logging
    with log_operation(logger, "data_processing", items_count=100):
        time.sleep(0.2)
    
    # Test retry logic
    attempt_count = 0
    @retry_with_backoff(logger, max_retries=3, base_delay=0.5)
    def flaky_function():
        global attempt_count
        attempt_count += 1
        if attempt_count < 3:
            # Simulate a transient failure on the first two attempts
            raise ValueError(f"Simulated transient error on attempt {attempt_count}")
        return "flaky_success"

    # Invoke the flaky function to demonstrate retry behavior
    try:
        result = flaky_function()
        logger.info("Flaky function completed successfully", result=result, attempts=attempt_count)
    except Exception as e:
        logger.error("Flaky function failed after retries", exception=e, attempts=attempt_count)