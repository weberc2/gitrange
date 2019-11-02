#! /usr/bin/env python

import ast
import sys
import os
import logging


def _find_usage(module: ast.Module) -> str:
    for node in module.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name) # pacify mypy
            and node.targets[0].id == "_usage"
            and isinstance(node.value, ast.Str)
        ):
            return node.value.s
    raise ValueError("Missing global variable '_usage'")


templates_directory = os.path.dirname(__file__)
repo_directory = os.path.dirname(templates_directory)

# Read in the contents of gr.py
gr_contents: str = ""
with open(os.path.join(repo_directory, "gr.py")) as f:
    gr_contents = f.read()

# Read in the contents of the README template
readme_contents: str = ""
with open(os.path.join(templates_directory, "README.md")) as f:
    readme_contents = f.read()

# Indent the usage by 4 spaces
_usage = ""
for line in _find_usage(ast.parse(gr_contents)).split("\n"):
    if len(line) > 0:
        _usage += "    "
    _usage += line + "\n"

# Parse gr.py, extract the usage text, and replace the '{{ _usage }}' token
# with the usage text
result = readme_contents.replace("{{ _usage }}", _usage)

# If we're in --check mode, then compare the existing README with the newly-
# rendered README and fail if there are differences
target_path = os.path.join(repo_directory, "README.md")
if len(sys.argv) > 1 and sys.argv[0] == "--check":
    contents = ""
    with open(target_path) as f:
        contents = f.read()
    if contents != result:
        print(f"{target_path} is out of date.", file=sys.stderr)
        sys.exit(1)
else:
    # Otherwise write the newly-rendered README back to the target path
    with open(target_path, "w") as f:
        f.write(result)
