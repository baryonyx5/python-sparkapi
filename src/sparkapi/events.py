"""Spark Events Class."""

from .base import BaseObject, BaseAPI
from .messages import Message
from .memberships import Membership


class Event(BaseObject):
    def __init__(self, event_data, whitelist=(), blacklist=()):
        self.id = event_data.pop('id')
        self.resource = event_data.pop('resource', '')
        self.type = event_data.pop('type', '')
        self.actorId = event_data.pop('actorId', '')
        self.orgId = event_data.pop('orgId', '')
        self.created = self.set_datetime(event_data.pop('created'))
        self.data = self._get_resource_data(event_data.pop('data'))
        super().__init__(event_data, whitelist, blacklist)

    def _get_resource_data(self, resource_data):
        if not resource_data:
            return None
        if self.resource == 'messages':
            return Message(resource_data, blacklist=('text', 'html'))
        elif self.resource == 'memberships':
            return Membership(resource_data)
        else:
            return None


# noinspection PyShadowingBuiltins
class Events(BaseAPI):
    DataClass = Event
    uri = 'events'

    def list_events(self, resource, event_type='created',
                    from_date=None, to_date=None, actorId=None,
                    max=None, blacklist=(), whitelist=()):
        params = {
            'resource': resource,
            'type': event_type,
            'from': from_date,
            'to': to_date,
            'actorId': actorId,
            'max': max
        }

        return self.list(blacklist, whitelist, **params)

    def get_event(self, id):
        return self.get_by_id(id)
