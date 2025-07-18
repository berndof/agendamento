#!/bin/bash
set -e

echo "Running with reload"

exec uv run --env-file ./.env.dev src/main.py --reload