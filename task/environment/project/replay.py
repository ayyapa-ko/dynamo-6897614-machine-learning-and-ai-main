import json
from typing import List, Dict, Any

def load_replay_trace(path: str) -> List[Dict[str, Any]]:
    """Load deterministic replay trace from JSON."""
    with open(path, 'r') as f:
        return json.load(f)
        
def generate_baseline_outputs(trace: List[Dict[str, Any]]) -> Dict[int, str]:
    """Generate expected outputs for each request in trace."""
    outputs = {}
    for req in trace:
        req_id = req['id']
        # Synthetic output: echo the prompt length and request id
        outputs[req_id] = f"output_for_req_{req_id}_prompt_len_{req['prompt_length']}"
    return outputs