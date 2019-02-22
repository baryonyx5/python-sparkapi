from requests.exceptions import HTTPError


class SparkAPIError(Exception):
    pass


class TooManyRequestsException(HTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.retry_after = int(self.response.headers['Retry-After'])
        except (KeyError, ValueError):
            self.retry_after = 60

