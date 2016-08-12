"""git-dump-all-trees

Usage:
  git-dump-all-trees (-h | --help)
  git-dump-all-trees --version
  git-dump-all-trees <output-root> <rev1> <rev2>

Options:
  -h --help    Show this help info
  --version    Display version info and exit

Write, to <output-root>, a collection of files which represent snapshots
of all commits reachable from <rev2> but not reachable from <rev1>.

The newly-created output directory contains two directories:

    blobs/ --- Contains one file per blob reachable from any commit in
        rev1..rev2.  Each blob resides in a directory named by the first
        two characters of the blob's SHA1.  The remaining 38 characters
        of the SHA1 give the filename within that directory.

    commit-trees/ --- Contains one directory per commit, in the same
        2/38 format as the blobs.  Each commit's directory contains the
        files and directories making up the tree corresponding to that
        commit.  (Files are hard links to the appropriate blob within
        the blobs directory; directories are real directories.)
"""

import os
import pygit2 as git
import docopt
import literategit.dump_all_trees
from literategit._version import __version__
from literategit.cli.repo_for_path import repo_for_path

def dump_all_trees():
    args = docopt.docopt(__doc__,
                         version='git-dump-all-trees {}'.format(__version__))
    repo = repo_for_path(os.getcwd())

    literategit.dump_all_trees.dump_all_trees(repo,
                                              args['<rev1>'], args['<rev2>'],
                                              args['<output-root>'])
