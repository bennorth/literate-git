# Copyright (C) 2016 Ben North
#
# This file is part of literate-git tools --- render a literate git repository
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""git-literate-render

Usage:
  git-literate-render (-h | --help)
  git-literate-render --version
  git-literate-render <title> <begin-commit> <end-commit> <create-url> [--no-results]

Options:
  -h --help     Show this help info
  --version     Display version info and exit
  --no\-results Don't add a results link to each commit

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
    repo_path = _path or os.getcwd()
    repo = repo_for_path(repo_path)

    sections = literategit.list_from_range(repo,
                                           args['<begin-commit>'],
                                           args['<end-commit>'])

    import_name, obj_name = args['<create-url>'].rsplit('.', 1)
    try:
        create_url_module = importlib.import_module(import_name)
    except ImportError:
        import sys
        sys.path.append(repo_path)
        create_url_module = importlib.import_module(import_name)

    create_url = getattr(create_url_module, obj_name)

    _print(literategit.render(sections, create_url, args['<title>'], not args['--no-results']))
