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

from functools import partial
import markdown2
import os
import pygit2 as git
from collections import namedtuple
import jinja2
import pygments
import pygments.lexers
import pygments.formatters

class NakedHtmlFormatter(pygments.formatters.HtmlFormatter):
    """A HTML formatter that doesn't wrap the lines in a <div>"""
    def wrap(self, source, outfile):
        for i, t in source:
            yield i, t


class TemplateSuite:
    def __init__(self, create_url, title, has_results=True):
        """
        Create a TemplateSuite instance from the given 'URL factory' and title.

        The 'create_url' argument should have attributes:

        result_url --- A callable which, given a commit SHA1, returns a URL for the
            'results' of the repo as of that commit.  The meaning of 'result' will vary
            from project to project.

        source_url --- A callable which, given a commit SHA1, returns a URL for the
            'source' of the repo as of that commit.  This could be a GitHub 'browse the
            tree at this commit' link, say, or some other presentation.

        The 'title' should be a string used as the content of the <title> and <h1>
        elements.  It is made available as the global 'project_title' within the
        constructed Jinja environment's templates.
        """
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
        env = jinja2.Environment(loader=loader)
        env.filters['as_html_fragment'] = self.as_html_fragment
        env.filters['result_url'] = create_url.result_url
        env.filters['source_url'] = create_url.source_url
        env.filters['diff_line_classification'] = Diff.line_classification
        env.filters['suppress_no_lineno'] = Diff.suppress_no_lineno
        env.filters['markdown'] = self.markdown
        env.filters['section_path'] = lambda path: '.'.join(map(str, path))
        env.globals['has_results'] = has_results
        env.globals['project_title'] = title
        self.node = env.get_template('node.html.tmpl')
        self.content = env.get_template('content.html.tmpl')
        self.diff = env.get_template('diff.html.tmpl')
        self.page = env.get_template('page.html.tmpl')

    def as_html_fragment(self, x):
        return x.as_html_fragment(self)

    @staticmethod
    def markdown(source_text):
        return jinja2.Markup(markdown2.markdown(source_text,
                                                extras=['fenced-code-blocks']))


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


class Node:
    def as_html_fragment(self, template_suite):
        # TODO: Add 'level' argument?
        return template_suite.node.render(node=self)

    @property
    def title(self):
        return self.commit.message.split('\n')[0]

    @property
    def message_body(self):
        return '\n'.join(self.commit.message.split('\n')[1:])

    @property
    def diff(self):
        return Diff(self.repo, self.commit.tree.oid, self.commit.parents[0].tree.oid)


class LeafCommit(namedtuple('LeafCommit', 'repo commit seqnum_path'), Node):
    @classmethod
    def from_commit(cls, repo, oid, seqnum_path):
        commit = _commit(repo, oid, 1, 'leaf-commit')
        return cls(repo, commit, seqnum_path)


class SectionCommit(namedtuple('SectionCommit', 'repo commit children seqnum_path'), Node):
    @classmethod
    def from_branch(cls, repo, branch_name, seqnum_path):
        return cls.from_commit(repo, repo.lookup_branch(branch_name).target, seqnum_path)

    @classmethod
    def from_commit(cls, repo, oid, seqnum_path):
        commit = _commit(repo, oid, 2, 'section-commit')
        prev_node = commit.parent_ids[0]
        ch = commit.parent_ids[1]
        children = []
        seqnum = n_steps_between(repo, ch, prev_node)
        while ch != prev_node:
            children.append(leaf_or_section(repo, ch, seqnum_path + [seqnum]))
            ch = repo[ch].parent_ids[0]
            seqnum -= 1
        children.reverse()
        return cls(repo, commit, children, seqnum_path)


class Diff(namedtuple('Diff', 'repo tree_1 tree_0')):
    formatter = NakedHtmlFormatter(linenos=False, wrapcode=True)

    def as_html_fragment(self, template_suite):
        diff = self.repo.diff(self.repo[self.tree_0], self.repo[self.tree_1])

        old_highlighted = self.collect_highlights(self.tree_0)
        new_highlighted = self.collect_highlights(self.tree_1)

        return template_suite.diff.render(diff=diff,
                                          old_highlighted=old_highlighted,
                                          new_highlighted=new_highlighted)

    def collect_highlights(self, tree):
        highlights = {}
        for entry in self.repo[tree]:
            blob = self.repo[entry.id]
            if blob.is_binary:
                continue
            text = blob.data.decode()
            lexer = pygments.lexers.get_lexer_for_filename(entry.name)
            lines = pygments.highlight(text, lexer, self.formatter).split('\n')
            highlights[entry.name] = lines
        return highlights

    @staticmethod
    def line_classification(line):
        if line.old_lineno == -1:
            return 'diff-add'
        elif line.new_lineno == -1:
            return 'diff-del'
        else:
            return 'diff-unch'

    @staticmethod
    def suppress_no_lineno(lineno):
        if lineno == -1:
            return ''
        return str(lineno)

def leaf_or_section(repo, oid, seqnum_path):
    commit = _commit(repo, oid)
    n_parents = len(commit.parent_ids)
    if n_parents == 1:
        return LeafCommit.from_commit(repo, oid, seqnum_path)
    elif n_parents == 2:
        return SectionCommit.from_commit(repo, oid, seqnum_path)
    else:
        raise ValueError('cannot handle {} parents of {}'
                         .format(n_parents, oid))

def n_steps_between(repo, begin_oid, end_oid):
    n = 0
    oid = begin_oid
    while oid != end_oid:
        n += 1
        oid = repo[oid].parent_ids[0]
    return n

def list_from_range(repo, base_branch_name, branch_name):
    end_oid = repo.lookup_branch(base_branch_name).target
    oid = repo.lookup_branch(branch_name).target
    elements = []
    seqnum = n_steps_between(repo, oid, end_oid)
    while oid != end_oid:
        element = leaf_or_section(repo, oid, [seqnum])
        elements.append(element)
        seqnum -= 1
        oid = element.commit.parent_ids[0]
    elements.reverse()
    return elements


def render(nodes, create_url, title, has_results=True):
    templates = TemplateSuite(create_url, title, has_results)
    style_defs = Diff.formatter.get_style_defs('.patch')
    content = templates.content.render(nodes=nodes, style_defs=style_defs)
    return templates.page.render(content=content)
