from typing import Tuple
from dataclasses import dataclass

@dataclass
class RoutingDecision:
    use_speculative: bool
    reason: str
    
class SpeculativeRouter:
    def __init__(self, speculative_threshold: int, kv_cache_capacity: int):
        self.speculative_threshold = speculative_threshold
        self.kv_cache_capacity = kv_cache_capacity
        self.current_kv_usage = 0
        
    def route(self, prompt_length: int, estimated_output_length: int) -> RoutingDecision:
        """
        Route request to speculative or standard autoregressive track.
        BUG: The comparison logic is inverted or has off-by-one error.
        """
        total_tokens_needed = prompt_length + estimated_output_length
        remaining_cache = self.kv_cache_capacity - self.current_kv_usage
        
        # BUG: This condition is backwards - should be >= not <
        if total_tokens_needed < self.speculative_threshold:
            if remaining_cache >= total_tokens_needed:
                self.current_kv_usage += total_tokens_needed
                return RoutingDecision(
                    use_speculative=True,
                    reason="Prompt length below speculative threshold and cache available"
                )
            else:
                return RoutingDecision(
                    use_speculative=False,
                    reason="Insufficient KV cache for speculative track"
                )
        else:
            # Standard autoregressive
            if remaining_cache >= total_tokens_needed:
                self.current_kv_usage += total_tokens_needed
                return RoutingDecision(
                    use_speculative=False,
                    reason="Using standard autoregressive track"
                )
            else:
                return RoutingDecision(
                    use_speculative=False,
                    reason="Cache overflow - forcing standard track"
                )
                
    def release_tokens(self, num_tokens: int):
        """Release tokens from KV cache after inference completes."""
        self.current_kv_usage = max(0, self.current_kv_usage - num_tokens)