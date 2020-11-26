import re
from setuptools import setup, find_packages

__version__ = re.findall(r"__version__\s*\=\s*'([\w\.\-]+)'",
                         open('literategit/_version.py').read())[0]

with open('long-description.md', 'rt') as f_in:
    long_description_md = f_in.read()

setup(
    name='literategit',
    version=__version__,
    author='Ben North',
    author_email='ben@redfrontdoor.org',
    description='Render a structured git history as an interactive web page',
    long_description=long_description_md,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        ],
    python_requires='>=3.5',
    url='https://github.com/bennorth/literate-git',
    install_requires=['pygit2==1.4.0', 'markdown2', 'jinja2<3.0.0', 'docopt', 'Pygments==2.5.2'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'beautifulsoup4'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['git-literate-render = literategit.cli:render',
                            'git-dump-all-trees = literategit.cli:dump_all_trees']},
)
