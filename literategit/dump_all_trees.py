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


class WriteBlobs:
    def __init__(self, repo, outdir):
        self.repo = repo
        self.outdir = outdir
        self.blobs = set()
        mkdir_excl(outdir)

    def ensure_exists(self, blob_oid):
        out_path_dirname = blob_oid.hex[:2]
        out_path_basename = blob_oid.hex[2:]
        full_dirname = os.path.join(self.outdir, out_path_dirname)
        full_filename = os.path.join(full_dirname, out_path_basename)
        if blob_oid not in self.blobs:
            if not os.path.exists(full_dirname):
                os.mkdir(full_dirname)
            with open(full_filename, 'wb') as f_out:
                data = self.repo[blob_oid].data
                f_out.write(data)
            self.blobs.add(blob_oid)
        return full_filename


class LinkTrees:
    def __init__(self, repo, write_blobs, outdir):
        self.repo = repo
        self.write_blobs = write_blobs
        self.outdir = outdir
        mkdir_excl(outdir)

    def new_nested(self, dirname):
        return self.__class__(self.repo,
                              self.write_blobs,
                              os.path.join(self.outdir, dirname))

    def new_nested_for_commit(self, commit):
        sha1 = commit.id.hex
        dirname = os.path.join(sha1[:2], sha1[2:])
        return self.new_nested(dirname)

    def create_all(self, tree_oid):
        for entry in self.repo[tree_oid]:
            if entry.type == 'blob':
                blob_filename = self.write_blobs.ensure_exists(entry.oid)
                os.link(blob_filename, os.path.join(self.outdir, entry.name))
            elif entry.type == 'tree':
                self.new_nested(entry.name).create_all(entry.oid)
            else:
                raise ValueError('unhandled type "{}"'.format(entry.type))


def dump_all_trees(repo, rev1, rev2, out_root):
    write_blobs = WriteBlobs(repo, os.path.join(out_root, 'blobs'))
    link_trees = LinkTrees(repo, write_blobs, os.path.join(out_root, 'commit-trees'))
    for c in collect_commits(repo, rev1, rev2):
        link_trees.new_nested_for_commit(c).create_all(c.tree.id)
