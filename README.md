# GitRange

Git is confusing. Most of us know the basics, but we all have to Google for
specific incantations from time to time. If you haven't used a different VCS,
like Mercurial, then you may not realize that this Googling for these somewhat
common things isn't normal or necessary--that it's a consequence of Git's
inconsistent UI.

GitRange (`gr`) attempts to bring some of that consistency to git by providing
a common syntax for specifying git commit ranges and passing those ranges to a
git subcommand.

## Usage

    USAGE: gr <selector> [<git-command>] [<git-command-args>]

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

        $ gr -c . null
        HEAD~1..HEAD


