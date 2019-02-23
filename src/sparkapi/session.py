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
class Session:
    CONTENT_TYPE = 'application/json'

    def __init__(self, access_token, timeout=None):
        self.access_token = access_token
        self.timeout = timeout
        self._session = requests.session()

    @property
    def headers(self):
        return {
            'Authorization': 'Bearer %s' % self.access_token,
            'Content-type': self.CONTENT_TYPE
        }

    def get(self, url, params=None):
        retries = 0
        while retries < 5:
            try:
                resp = resp_or_exception(
                    self._session.get(
                        url=url, headers=self.headers, params=params, timeout=self.timeout))
            except exc.TooManyRequestsException as ex:
                retry = ex.retry_after
                log.warning('429: Too Many Requests received. Waiting %s seconds', retry)
                retries += 1
                time.sleep(retry)
            else:
                return resp
        raise exc.SparkAPIError('Too Many Consecutive Retries (%d) for %s', retries, url)

    def post(self, url, payload=None):
        resp = self._session.post(url, headers=self.headers, json=payload, timeout=self.timeout)
        return resp_or_exception(resp)

    def put(self, url, payload=None):
        resp = self._session.put(url, headers=self.headers, json=payload, timeout=self.timeout)
        return resp_or_exception(resp)

    def delete(self, url):
        resp = self._session.delete(url, headers=self.headers, timeout=self.timeout)
        return resp_or_exception(resp)
