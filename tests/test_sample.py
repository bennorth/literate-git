import pygit2 as git
import pytest

tamagotchi_github_url = 'https://github.com/bennorth/webapp-tamagotchi.git'


@pytest.fixture(scope='session')
def tamagotchi_repo(tmpdir_factory):
    repo_root = str(tmpdir_factory.mktemp('repo'))
    repo = git.clone_repository(tamagotchi_github_url, repo_root, checkout_branch='for-rendering')
    branch = repo.lookup_branch('origin/start', git.GIT_BRANCH_REMOTE)
    commit = repo[branch.target]
    repo.create_branch('start', commit)
    return repo
