set +x

repoRoot=$(dirname "$0")

# Typecheck
mypy --strict . > /dev/null
mypy --strict ./templates > /dev/null

# Format check (all python files in the repo)
black --check --quiet .

# Check README.md
$repoRoot/templates/mkreadme.py --check
