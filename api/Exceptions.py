class YQLQueryError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Query failed with error: "%s"' % repr(self.value)


class YQLResponseMalformedError(Exception):

    def __str__(self):
        return 'Malformed response'
