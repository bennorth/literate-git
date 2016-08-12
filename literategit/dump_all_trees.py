import os


def collect_commits(repo, rev1, rev2):
    """
    List of all Commit objects which are reachable from rev2 but not
    reachable from rev1.  Commits are not returned in any particular
    order.
    """
    walker = repo.walk(repo.revparse_single(rev2).id)
    walker.hide(repo.revparse_single(rev1).id)
    return list(walker)


def mkdir_excl(dirname):
    if os.path.exists(dirname):
        raise ValueError('directory "{}" already exists'
                         .format(dirname))
    os.makedirs(dirname)
