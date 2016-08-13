"""git-literate-render

Usage:
  git-literate-render (-h | --help)
  git-literate-render --version
  git-literate-render <title> <begin-commit> <end-commit> <create-url>

Options:
  -h --help    Show this help info
  --version    Display version info and exit

Write, to stdout, an HTML representation of the repo history starting
from (but excluding) <begin-commit> and ending, inclusively, with
<end-commit>.

The <create-url> argument should be in the form

    possibly.nested.package.object

where 'object' within the importable 'possibly.nested.package' should
have callable attributes 'result_url' and 'source_url'.  For example,
'object' can be a class with the given 'staticmethod's.  For more
details see the code (TemplateSuite).

The <title> argument provides the contents of the <title> and <h1>
elements in the rendered output.
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
    try:
        create_url_module = importlib.import_module(import_name)
    except ImportError:
        import sys
        sys.path.append(_path or os.getcwd())
        create_url_module = importlib.import_module(import_name)

    create_url = getattr(create_url_module, obj_name)

    _print(literategit.render(sections, create_url, args['<title>']))
