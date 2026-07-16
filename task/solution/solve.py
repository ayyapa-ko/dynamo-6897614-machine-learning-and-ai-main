#!/usr/bin/env python3
"""
Reference solution for ML serving debug task.
Applies corrections to:
1. config.yaml - reduce max_batch_delay from 500ms to 20ms
2. router.py - fix inverted logic in speculative routing threshold check
"""

import yaml
from pathlib import Path

def fix_config():
    """Fix configuration: reduce max_batch_delay to prevent starvation."""
    config_path = Path('/app/project/config.yaml')
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Fix: Change from 500ms to 20ms to prevent request starvation
    config['max_batch_delay'] = 20
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print("[FIXED] config.yaml: max_batch_delay changed to 20ms")

def fix_router():
    """Fix router.py: correct the inverted threshold comparison logic."""
    router_path = Path('/app/project/router.py')
    
    content = router_path.read_text()
    
    # Fix: Change 'total_tokens_needed < self.speculative_threshold' to '>='
    # This ensures requests with prompt length >= threshold use speculative path
    content = content.replace(
        'if total_tokens_needed < self.speculative_threshold:',
        'if total_tokens_needed >= self.speculative_threshold:'
    )
    
    router_path.write_text(content)
    
    print("[FIXED] router.py: corrected speculative threshold comparison logic")

def verify_fixes():
    """Run benchmark to verify fixes work."""
    import subprocess
    result = subprocess.run(
        ['python3', '/app/project/benchmark.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("[SUCCESS] Benchmark completed successfully")
        print(result.stdout)
    else:
        print("[ERROR] Benchmark failed")
        print(result.stderr)
        raise RuntimeError("Benchmark verification failed")

if __name__ == '__main__':
    fix_config()
    fix_router()
    verify_fixes()
    print("\n✓ All fixes applied and verified")