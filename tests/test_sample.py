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

import bs4
import pygit2 as git
import pytest
import hashlib

import literategit.cli
import literategit.dump_all_trees


tamagotchi_github_url = 'https://github.com/bennorth/webapp-tamagotchi.git'


@pytest.fixture(scope='session')
def local_repo(tmpdir_factory):
    repo_root = str(tmpdir_factory.mktemp('repo'))
    repo = git.clone_repository('.', repo_root, checkout_branch='sample-history-for-tests')
    branch = repo.lookup_branch('origin/initial-empty-state', git.GIT_BRANCH_REMOTE)
    commit = repo[branch.target]
    repo.create_branch('start', commit)
    branch = repo.lookup_branch('origin/test-point-without-docs', git.GIT_BRANCH_REMOTE)
    commit = repo[branch.target]
    repo.create_branch('test-point-without-docs', commit)
    return repo


class TestLocalRepo:
    def test_render(self, local_repo):
        args = ['My cool project', 'start', 'sample-history-for-tests',
                'literategit.example_create_url.CreateUrl']
        output_list = []
        literategit.cli.render(_argv=args,
                               _path=local_repo.path,
                               _print=output_list.append)
        assert len(output_list) == 1
        output_text = output_list[0]
        assert 'Add documentation' in output_text
        assert 'Add <code>colours</code> submodule' in output_text

        # Regression test.  The previous two asserts are therefore unnecessary
        # (as long as they passed while setting this hash), but leaving them in
        # for clarity.
        #
        output_hash = hashlib.sha256(output_text.encode()).hexdigest()
        exp_hash = 'e5f914e3e66a8714620bb7e4bd2a76e3c263cac045787a6284240774a7d353d2'
        assert output_hash == exp_hash


@pytest.fixture(scope='session')
def tamagotchi_repo(tmpdir_factory):
    repo_root = str(tmpdir_factory.mktemp('repo'))
    repo = git.clone_repository(tamagotchi_github_url, repo_root, checkout_branch='for-rendering')
    branch = repo.lookup_branch('origin/start', git.GIT_BRANCH_REMOTE)
    commit = repo[branch.target]
    repo.create_branch('start', commit)
    return repo


class TestTamagotchi:
    def test_render(self, tamagotchi_repo):
        """
        This is fragile in that it relies on the exact state of the 'Tamagotchi'-style
        webapp repo, but it does at least check all the parts fit together.
        """
        args = ['My cool project', 'start', 'for-rendering', 'literategit.example_create_url.CreateUrl']
        output_list = []
        literategit.cli.render(_argv=args,
                               _path=tamagotchi_repo.path,
                               _print=output_list.append)

        assert len(output_list) == 1
        output_text = output_list[0]

        soup = bs4.BeautifulSoup(output_text, 'html.parser')
        node_divs = soup.find_all('div', class_='literate-git-node')
        got_sha1s = sorted(d.attrs['data-commit-sha1'] for d in node_divs)

        exp_commits = literategit.dump_all_trees.collect_commits(tamagotchi_repo,
                                                                 'start',
                                                                 'for-rendering')
        exp_sha1s = sorted(c.hex for c in exp_commits)

        assert got_sha1s == exp_sha1s
        assert len(got_sha1s) == 162  # More fragility

        # Regression test.
        output_hash = hashlib.sha256(output_text.encode()).hexdigest()
        exp_hash = 'de1fe41a6625690806b76678d4f8b68c59c9c587b4e8720092c1db67a8527b46'
        assert output_hash == exp_hash
