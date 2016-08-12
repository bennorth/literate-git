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
