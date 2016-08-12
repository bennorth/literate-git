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
