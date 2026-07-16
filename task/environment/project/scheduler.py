import time
import json
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Request:
    id: int
    arrival_time: float
    prompt_length: int
    
class BatchScheduler:
    def __init__(self, max_batch_size: int, max_batch_delay: int):
        self.max_batch_size = max_batch_size
        self.max_batch_delay = max_batch_delay / 1000.0  # convert ms to seconds
        self.queue: List[Request] = []
        self.batch_start_time: float = None
        self.starvation_events = 0
        
    def add_request(self, request: Request):
        """Add request to queue and initialize batch timer if needed."""
        self.queue.append(request)
        if self.batch_start_time is None:
            self.batch_start_time = request.arrival_time
            
    def should_dispatch(self, current_time: float) -> bool:
        """Check if batch should be dispatched."""
        if not self.queue:
            return False
            
        # Dispatch if batch is full
        if len(self.queue) >= self.max_batch_size:
            return True
            
        # Dispatch if max delay exceeded
        if self.batch_start_time is not None:
            elapsed = current_time - self.batch_start_time
            if elapsed >= self.max_batch_delay:
                if len(self.queue) > 0:
                    self.starvation_events += 1
                return True
                
        return False
        
    def get_batch(self) -> List[Request]:
        """Return current batch and reset queue."""
        batch = self.queue[:self.max_batch_size]
        self.queue = self.queue[self.max_batch_size:]
        self.batch_start_time = None if not self.queue else time.time()
        return batch