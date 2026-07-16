#!/bin/bash
#
# Runs inside the SHARED environment image. 
# All testing dependencies are baked into the image layers.

# Create target verifier directories if missing
mkdir -p /logs/verifier

# Execute tests and generate the standard JSON report
pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA

# Track the structural validation output status for Harbor mapping
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi