class HardCodedCreateUrl:
    @staticmethod
    def result_url(oid):
        sha1 = oid.hex
        # TODO: Allow specification of what 'result' means for a particular project.
        return 'commit-trees/{}/{}/page.html'.format(sha1[:2], sha1[2:])

    @staticmethod
    def source_url(oid):
        sha1 = oid.hex
        # TODO: Proper configuration for this.
        return 'https://github.com/bennorth/webapp-tamagotchi/tree/{}'.format(sha1)
