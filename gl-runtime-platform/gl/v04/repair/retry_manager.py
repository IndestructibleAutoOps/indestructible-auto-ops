"""GL Runtime V4 - 重試管理器"""
from typing import Any, Callable, Optional
from dataclasses import dataclass
import time

@dataclass
class RetryConfig:
    max_attempts: int = 3
    delay: float = 1.0
    backoff: float = 2.0

class RetryManager:
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        last_error = None
        delay = self.config.delay
        for attempt in range(self.config.max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                time.sleep(delay)
                delay *= self.config.backoff
        raise last_error
