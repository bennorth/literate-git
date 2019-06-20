class CreateUrl:
    @staticmethod
    def result_url(sha1):
        return 'http://example.com/results/{}'.format(sha1)

    @staticmethod
    def source_url(sha1):
        return 'http://example.com/source/{}'.format(sha1)
