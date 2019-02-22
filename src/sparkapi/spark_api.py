"""CiscoSparkAPI init."""
import logging
import time
import requests
from json import JSONDecodeError
from .people import People
from .roles import Roles
from .rooms import Rooms
from .messages import Messages
from .metrics import Metrics
from .teams import Teams
from .memberships import Memberships
from .team_memberships import TeamMemberships
from .organizations import Organizations
from .licenses import Licenses
from .events import Events
from .webhooks import WebHooks
from sparkapi.exc import TooManyRequestsException, HTTPError, SparkAPIError


def resp_or_exception(response):
    """Raises stored :class:`HTTPError`, if one occurred."""
    if response.ok:
        return response
    elif response.status_code == 429:
        raise TooManyRequestsException(response.reason, response=response)
    else:
        try:
            msg = response.json().get('message', '')
        except JSONDecodeError:
            msg = ''
        err_txt = 'Error: %s, %s, %s for url: %s' % (response.status_code,
                                                     response.reason,
                                                     msg,
                                                     response.url)
        raise HTTPError(err_txt, response=response)


# noinspection PyShadowingBuiltins
class RestSession:
    CONTENT_TYPE = "application/json"

    def __init__(self, access_token=None, timeout=None):
        self.access_token = access_token
        self.timeout = timeout
        self._session = requests.session()

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.access_token}",
                "Content-type": f"{self.CONTENT_TYPE}"}

    def get(self, base_url, params=None, id=None):
        url = base_url
        if id:
            url = url + "/" + id
        retries = 0
        while retries < 5:
            try:
                resp = resp_or_exception(
                        self._session.get(url=url, headers=self.headers,
                                          params=params, timeout=self.timeout))
            except TooManyRequestsException as ex:
                retry = ex.retry_after
                logging.warning('429: Too Many Requests received. Waiting %s seconds', retry)
                retries += 1
                time.sleep(retry)
            else:
                return resp
        raise SparkAPIError('Too Many Consecutive Retries (%d) for %s', retries, url)

    def post(self, base_url, payload=None, id=None):
        url = base_url
        if id:
            url = url + "/" + id
        resp = self._session.post(url, headers=self.headers,
                                  json=payload, timeout=self.timeout)
        return resp_or_exception(resp)

    def put(self, base_url, payload=None, id=None):
        url = base_url
        if id:
            url = url + "/" + id
        resp = self._session.put(url, headers=self.headers,
                                 json=payload, timeout=self.timeout)
        return resp_or_exception(resp)

    def delete(self, base_url, id):
        url = base_url + "/" + id
        resp = self._session.delete(url, headers=self.headers,
                                    timeout=self.timeout)
        return resp_or_exception(resp)


# noinspection PyPep8Naming
class SparkAPI:
    """
    """
    BASE_URL = 'https://api.ciscospark.com/v1/'

    def __init__(self, access_token, orgId=None, timeout=360, debug=False):
        """
        """
        self.access_token = access_token
        self.orgId = orgId
        self.timeout = timeout
        self.debug = debug
        self.session = RestSession(self.access_token, self.timeout)
        self.people = People(self.session, self.BASE_URL, self.orgId, url_suffix='people')
        self.roles = Roles(self.session, self.BASE_URL, self.orgId, url_suffix='roles')
        self.rooms = Rooms(self.session, self.BASE_URL, self.orgId, url_suffix='rooms')
        self.teams = Teams(self.session, self.BASE_URL, self.orgId, url_suffix='teams')
        self.messages = \
            Messages(self.session, self.BASE_URL, self.orgId, url_suffix='messages')
        self.licenses = \
            Licenses(self.session, self.BASE_URL, self.orgId, url_suffix='licenses')
        self.events = Events(self.session, self.BASE_URL, self.orgId, url_suffix='events')
        self.memberships = \
            Memberships(self.session, self.BASE_URL, self.orgId, url_suffix='memberships')
        self.metrics = \
            Metrics(self.session, self.BASE_URL, self.orgId, url_suffix='metrics/adhoc?')
        self.webhooks = \
            WebHooks(self.session, self.BASE_URL, self.orgId, url_suffix='webhooks')
        self.team_memberships = \
            TeamMemberships(self.session, self.BASE_URL, self.orgId,
                            url_suffix='team/memberships')
        self.organizations = \
            Organizations(self.session, self.BASE_URL, self.orgId,
                          url_suffix='organizations')
