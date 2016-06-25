import pygit2 as git
from collections import namedtuple


def _commit(repo, oid, required_n_parents=None, tag=None):
    commit = repo[oid]
    if not isinstance(commit, git.Commit):
        raise ValueError('not a Commit')
    parent_ids = commit.parent_ids
    n_parents = len(parent_ids)
    if required_n_parents is not None and n_parents != required_n_parents:
        raise ValueError('commit {} has {} parent/s so is not a {}'
                         .format(oid, n_parents, tag))
    return commit


class LeafCommit(namedtuple('LeafCommit', 'repo commit')):
    pass


class SectionCommit(namedtuple('SectionCommit', 'repo commit children')):
    pass
