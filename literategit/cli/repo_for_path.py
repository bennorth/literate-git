import pygit2 as git


def repo_for_path(dirname):
    try:
        return git.Repository(git.discover_repository(dirname, False))
    except KeyError:
        raise ValueError('could not find git repo starting from {}'.format(dirname))
