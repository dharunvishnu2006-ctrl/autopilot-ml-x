#!/usr/bin/env bash
set -euo pipefail

PYTHON="./venv/Scripts/python.exe"

echo "Running black..."
$PYTHON -m black --check src tests app.py

echo "Running flake8..."
$PYTHON -m flake8 src app.py scripts tests

echo "Running mypy..."
$PYTHON -m mypy src

echo "Running bandit..."
$PYTHON -m bandit -r src -q

echo "Running tests..."
$PYTHON -m pytest -q

echo "✓ all gates passed"