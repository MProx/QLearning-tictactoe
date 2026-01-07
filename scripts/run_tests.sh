#! /bin/bash

set -e

cd $PWD/..

echo "Linting:"
uv run ruff check .
uv run ruff format --check .

echo "Type checking:"
uv run mypy .

echo "Unit tests:"
uv run pytest .

echo "All tests passed!"
