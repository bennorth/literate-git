class CreateUrl:
    @staticmethod
    def result_url(sha1):
        return 'http://example.com/results/{}'.format(sha1)

    @staticmethod
    def source_url(sha1):
        return 'http://example.com/source/{}'.format(sha1)


class CreateQueryUrl:
    @staticmethod
    def result_url(sha1):
        return 'http://example.com/results/?colour=blue&sha1={}'.format(sha1)

    @staticmethod
    def source_url(sha1):
        return 'http://example.com/source/{}'.format(sha1)
