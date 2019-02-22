"""Spark Parent Classes."""

from typing import List
from abc import ABCMeta
from collections import MutableMapping
import arrow
import logging
import base64
import re
import time
from sparkapi.exc import TooManyRequestsException, SparkAPIError

log = logging.getLogger('|.{}'.format(__name__.split('.')[-1]))


class SparkDataClass(MutableMapping):
    __metaclass__ = ABCMeta
    _format = 'YYYY-MM-DDTHH:mm:ss'

    def __init__(self, data, whitelist=(), blacklist=()):
        if whitelist:
            data = {k: v for k, v in data.items() if k in whitelist}
        elif blacklist:
            data = {k: v for k, v in data.items() if k not in blacklist}
        for k, v in data.items():
            setattr(self, k, v)

    @staticmethod
    def set_str(value):
        return str(value)

    @staticmethod
    def set_int(value):
        return int(value)

    @staticmethod
    def set_bool(value):
        return bool(value)

    def set_datetime(self, value, fmt=None):
        if value is None:
            return None
        if fmt is None:
            fmt = self._format
        naive_ts = arrow.get(value, fmt).naive
        return arrow.get(naive_ts).to('utc').datetime

    def decode_list(self, values):
        return [p for p in values]

    def decode_id(self, value):
        """Convert base64 Spark  ID to ciscospark:// URI and return guid"""
        value = str(value).strip()
        if not value:
            return ''
        try:
            uri = base64.b64decode(value)
            uri = uri.decode('utf-8')
        except Exception as e:
            if len(value) % 4 == 2:
                return self.decode_id(value + '==')
            elif len(value) % 4 == 3:
                return self.decode_id(value + '=')
            else:
                # not a padding issue so something else must be wrong
                raise TypeError('ID {} is invalid base64 {}'.format(value, e))
        else:
            m = re.search(r'ciscospark://\w+/\w+/(\S+)$', uri)
            if m:
                return m.group(1)
            else:
                raise ValueError('Could not derive guid from {}'.format(uri))

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def get(self, k, default=None):
        return self.__dict__.get(k, default)

    def __getitem__(self, k):
        return self.__dict__[k]

    def __setitem__(self, k, v):
        setattr(self, k, v)

    def __delitem__(self, k):
        delattr(self, k)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "%s" % self.__class__


# noinspection PyShadowingBuiltins
class SparkAPI:

    DataClass = SparkDataClass

    def __init__(self, session, base_url, orgId, url_suffix=''):
        self.session = session
        self.orgId = orgId
        self.url = base_url + url_suffix

    def list(self, blacklist=(), whitelist=(), **kwargs):
        params = {}
        params.update({k: v for k, v in kwargs.items() if v is not None})
        url = self.url
        data = []
        incr = 1
        while url:
            resp = self.session.get(url, params=params)
            incr_data = [self.DataClass(d, blacklist, whitelist) for d in resp.json()['items']]
            data += incr_data
            incr += 1
            url = resp.links.get('next', {}).get('url')
            params = {}
        return data

    def get_by_id(self, id, blacklist=(), whitelist=()) -> DataClass:
        resp = self.session.get(self.url, id=id)
        return self.DataClass(resp.json(), blacklist, whitelist)

    def delete(self, id):
        resp = self.session.delete(self.url, id=id)
        return resp

    @staticmethod
    def _id_or_email(param_list):
        for param, val in param_list:
            if val:
                return {param: val}
        raise SparkAPIError('One of %s must be provided' % ','.join([p[0] for p in param_list]))
