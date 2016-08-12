"""git-literate-render

Usage:
  git-literate-render (-h | --help)
  git-literate-render --version
  git-literate-render <begin-commit> <end-commit> <create-url>

Options:
  -h --help    Show this help info
  --version    Display version info and exit

Write, to stdout, an HTML representation of the repo history starting
from (but excluding) <begin-commit> and ending, inclusively, with
<end-commit>.
"""

import os
import importlib
import docopt
import literategit
from literategit._version import __version__
from literategit.cli.repo_for_path import repo_for_path


def render(_argv=None, _path=None, _print=print):
    args = docopt.docopt(__doc__, argv=_argv,
                         version='git-literate-render {}'.format(__version__))
    repo = repo_for_path(_path or os.getcwd())

    sections = literategit.list_from_range(repo,
                                           args['<begin-commit>'],
                                           args['<end-commit>'])

    import_name, obj_name = args['<create-url>'].rsplit('.', 1)
    create_url_module = importlib.import_module(import_name)
    create_url = getattr(create_url_module, obj_name)

    _print(literategit.render(sections, create_url))
