import re
from setuptools import setup, find_packages

__version__ = re.findall(r"__version__\s*\=\s*'([\w\.\-]+)'",
                         open('literategit/_version.py').read())[0]

setup(
    name='literategit',
    version=__version__,
    install_requires=['pygit2', 'markdown2', 'jinja2', 'docopt'],
    tests_require=['pytest', 'beautifulsoup4'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['git-literate-render = literategit.cli:render',
                            'git-dump-all-trees = literategit.cli:dump_all_trees']},
)
