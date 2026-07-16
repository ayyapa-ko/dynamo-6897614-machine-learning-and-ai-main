#!/bin/bash
#
# Reference (Oracle) solution execution harness for Harbor.
# Mounts solution/ at /solution/ and runs this script to prove task solvability.

# Run the python-based inline correction suite
python3 /solution/solve.py

echo "Oracle execution complete. System optimization applied successfully."