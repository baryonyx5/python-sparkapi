"""Spark Parent Classes."""

import re
import arrow
import base64
import logging
from typing import List
from abc import ABCMeta
from sparkapi.session import Session
from sparkapi.exc import SparkAPIError

log = logging.getLogger(__name__)


class BaseObject(metaclass=ABCMeta):
    _format = 'YYYY-MM-DDTHH:mm:ss'
    _id_attr = 'id'

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
        return '%s(id=%s)' % (self.__class__, getattr(self, self._id_attr, ''))

    def __str__(self):
        return self.__repr__()


# noinspection PyShadowingBuiltins
class BaseAPI:
    BASE_URL = 'https://api.ciscospark.com/v1/'
    DataClass = BaseObject
    uri = ''

    def __init__(self, session: Session):
        self.session = session

    def url(self, id=None):
        uri = self.uri.lstrip('/')
        url = self.BASE_URL + '/' + uri
        if id:
            return url + '/' + id
        return url

    def list(self, blacklist=(), whitelist=(), **kwargs) -> List[DataClass]:
        params = {}
        params.update({k: v for k, v in kwargs.items() if v is not None})
        url = self.url()
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
        resp = self.session.get(self.url(id))
        return self.DataClass(resp.json(), blacklist, whitelist)

    def delete(self, id):
        resp = self.session.delete(self.url(id))
        return resp

    @staticmethod
    def _id_or_email(**kwargs):
        for param, val in kwargs:
            if val:
                return {param: val}
        raise SparkAPIError('One of %s must be provided' % ','.join(list(kwargs.keys())))
