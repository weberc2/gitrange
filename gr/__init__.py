#! /usr/bin/env python
import subprocess
from typing import Tuple

_usage = """USAGE: gr <selector> [<git-command>] [<git-command-args>]

  Invoke a git command with a more sane range-selection syntax.

SELECTORS

  -b, --branch <commit-id>  A range of commits from <commit-id> to the common
                            ancestor of <commit-id> and `master`.

  -c, --commit <commit-id>  Exactly the commit identified by <commit-id>.

COMMIT ID SYNTAX

  `.`, `0`                  The current commit.

  <branch-name>             The name of the git branch. Resolves to the
                            branch's tip.

  <commit-sha>              A git commit sha.

  <tag>                     A git tag.

  (nonpositive integers)    A relative number of parent commits from `.`.
                            Positive integers are an error.

OTHER ARGUMENTS

  git-command               The git command to invoke with the range resulting
                            from the provided selector. If this is missing, the
                            range will be printed directly (useful for
                            debugging). This should not include the "git"
                            (e.g., "log", not "git log").

  git-command-args          The arguments to the git command. These will be
                            passed to <git-command> before the range.

EXAMPLES

  Log all changes in a branch:

    $ gr -b my-feature-branch log

  Log all changes in the current branch

    $ gr -b . log

  Diff a single changeset (against its parent):

    $ gr -c <git-sha1> diff

  Diff the current changeset (against its parent):

    $ gr -c . diff

  Diff an entire branch

    $ gr -b my-feature-branch diff

  Diff the current branch up to the parent commit

    $ gr -b -1 diff
    diff --git a/bar b/bar
    new file mode 100644
    index 0000000000..e69de29bb2
    diff --git a/foo b/foo
    new file mode 100644
    index 0000000000..e69de29bb2

  Pass other arguments

    $ gr -b . log --oneline --graph --decorate
    * dd6e2ccff4 (HEAD -> my-feature-branch) Removed foo and bar
    * 357bc24de5 Added bar
    * 8dd48a84d0 Added foo

  Debug a range

    $ gr -c .
    HEAD~1..HEAD
"""


def normalize_commit(commit: str) -> str:
    if commit in (".", "0"):
        return "HEAD"
    try:
        offset = int(commit)
        if offset < 0:
            return f"HEAD~{-1*offset}"
        else:
            raise Exception("Positive relative offsets are invalid")
    except ValueError:
        return commit


def evaluate_range(selector: str, argument: str) -> Tuple[str, str]:
    if selector in ("-c", "--commit"):
        return f"{argument}~1", argument
    if selector in ("-b", "--branch"):
        return (
            subprocess.run(
                ["git", "merge-base", "master", argument],
                check=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
            ).stdout.rstrip("\n"),
            argument,
        )
    raise Exception(f"Unknown selector: {selector}")


def main():
    import sys

    if len(sys.argv) < 3:
        print(_usage, file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] in ("-h", "--help"):
        print(_usage)
        sys.exit(0)

    start, end = evaluate_range(sys.argv[1], normalize_commit(sys.argv[2]))
    range_ = f"{start}..{end}"
    if len(sys.argv) < 4:
        print(range_)
        sys.exit(0)
    else:
        result = subprocess.run(["git"] + sys.argv[3:] + [range_])
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
