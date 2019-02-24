"""SparkAPI Request Session."""
import logging
import time
import requests
from json import JSONDecodeError
from sparkapi import exc

log = logging.getLogger(__name__)


def resp_or_exception(response):
    """Raises stored :class:`HTTPError`, if one occurred."""
    if response.ok:
        return response
    elif response.status_code == 429:
        raise exc.TooManyRequestsException(response.reason, response=response)
    else:
        try:
            msg = response.json().get('message', '')
        except JSONDecodeError:
            msg = ''
        err_txt = 'Error: %s, %s, %s for url: %s' % (
            response.status_code, response.reason,
            msg, response.url
        )
        raise exc.HTTPError(err_txt, response=response)


# noinspection PyShadowingBuiltins
class Session(requests.Session):

    def __init__(self, access_token, timeout=None):
        super().__init__()
        self.access_token = access_token
        self.timeout = timeout
        self.headers['Authorization'] = 'Bearer %s' % self.access_token
        self.headers['Content-type'] = 'application/json'

    def get(self, url, params=None, **kwargs):
        retries = 0
        while retries < 5:
            try:
                resp = resp_or_exception(super().get(url=url, params=params, **kwargs))
            except exc.TooManyRequestsException as ex:
                retry = ex.retry_after
                log.warning('429: Too Many Requests received. Waiting %s seconds', retry)
                retries += 1
                time.sleep(retry)
            else:
                return resp
        raise exc.SparkAPIError('Too Many Consecutive Retries (%d) for %s', retries, url)

    def post(self, url, params=None, data=None, json=None, **kwargs):
        resp = super().post(url, data=data, json=json, **kwargs)
        return resp_or_exception(resp)

    def put(self, url, params=None, data=None, json=None, **kwargs):
        resp = super().put(url, params=params, data=data, json=json, **kwargs)
        return resp_or_exception(resp)

    def delete(self, url, **kwargs):
        return resp_or_exception(super().delete(url, **kwargs))
