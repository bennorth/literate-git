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
    @classmethod
    def from_commit(cls, repo, oid):
        commit = _commit(repo, oid, 1, 'leaf-commit')
        return cls(repo, commit)


class SectionCommit(namedtuple('SectionCommit', 'repo commit children')):
    @classmethod
    def from_commit(cls, repo, oid):
        commit = _commit(repo, oid, 2, 'section-commit')
        prev_node = commit.parent_ids[0]
        ch = commit.parent_ids[1]
        children = []
        while ch != prev_node:
            children.append(leaf_or_section(repo, ch))
            ch = repo[ch].parent_ids[0]
        children.reverse()
        return cls(repo, commit, children)


def leaf_or_section(repo, oid):
    commit = _commit(repo, oid)
    n_parents = len(commit.parent_ids)
    if n_parents == 1:
        return LeafCommit.from_commit(repo, oid)
    elif n_parents == 2:
        return SectionCommit.from_commit(repo, oid)
    else:
        raise ValueError('cannot handle {} parents of {}'
                         .format(n_parents, oid))
