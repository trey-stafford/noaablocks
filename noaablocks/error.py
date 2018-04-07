class NotConnectedError(Exception):
    def __init__(self):

        message = 'Not connected to the Internet.'
        super().__init__(message)


class ServiceUnavailable(Exception):
    def __init__(self, url):

        message = 'Could not connect to {}'.format(url)
        super().__init__(message)


class ServiceError(Exception):
    def __init__(self, status_code, url):

        message = 'Recieved unexpected {} response from {}'.format(status_code, url)
        super().__init__(message)
