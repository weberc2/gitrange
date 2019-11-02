#! /usr/bin/env bash
#
# Requires: [ git, black, mypy ]
set +x

# Typecheck
mypy --strict $(find . -name \*.py) > /dev/null

# Format check (all python files in the repo)
black --check --quiet .

# Lint
flake8

# Check README.md
repoRoot=$(dirname "$0")
$repoRoot/gen/mkreadme.py --check
