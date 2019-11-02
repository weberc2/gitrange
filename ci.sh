#! /usr/bin/env bash
#
# Requires: [ git, black, mypy ]
set +x

# Typecheck
mypy --strict $(find . -name \*.py) > /dev/null

# Lint
flake8
isort --check --quiet
black --check --quiet .


# Check README.md
repoRoot=$(dirname "$0")
$repoRoot/gen/mkreadme.py --check
