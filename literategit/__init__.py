import os
import pygit2 as git
from collections import namedtuple
import jinja2


_templates = None
def templates():
    global _templates
    if _templates is None:
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
        env = jinja2.Environment(loader=loader)
        env.filters['as_html_fragment'] = as_html_fragment
        _templates = {'node': env.get_template('node.html.tmpl'),
                      'page': env.get_template('page.html.tmpl')}
    return _templates


def as_html_fragment(x):
    return x.as_html_fragment()


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
    def from_branch(cls, repo, branch_name):
        return cls.from_commit(repo, repo.lookup_branch(branch_name).target)

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


def list_from_range(repo, base_branch_name, branch_name):
    end_oid = repo.lookup_branch(base_branch_name).target
    oid = repo.lookup_branch(branch_name).target
    elements = []
    while oid != end_oid:
        element = leaf_or_section(repo, oid)
        elements.append(element)
        oid = element.commit.parent_ids[0]
    elements.reverse()
    return elements
