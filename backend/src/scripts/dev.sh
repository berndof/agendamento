#!/bin/bash
set -e

echo "Running with reload"

exec uv run src/main.py --reload