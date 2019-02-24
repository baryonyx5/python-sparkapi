"""Spark Room Classes."""

from .base import BaseObject, BaseAPI


class Room(BaseObject):
    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.title = data.pop('title', '')
        self.type = data.pop('type', '')
        self.creatorId = data.pop('creatorId', '')
        self.teamId = data.pop('teamId', '')
        self.isLocked = self.set_bool(data.pop('isLocked'))
        self.lastActivity = self.set_datetime(data.pop('lastActivity', None))
        self.created = self.set_datetime(data.pop('created'))
        super().__init__(data, whitelist, blacklist)

    def __repr__(self):
        return 'Room(title=%s, type=%s, id:%s)' % (self.title, self.type, self.id)


# noinspection PyShadowingBuiltins
class Rooms(BaseAPI):
    DataClass = Room
    uri = 'rooms'

    def get_by_title(self, title, type=None, max=None):
        data = self.list(type=type, max=max)
        return [d for d in data if d.get('title') == title]

    def get_by_team(self, teamId, type=None, max=None):
        data = self.list(teamId=teamId, type=type, max=max)
        return [d for d in data if d.get('teamId') == teamId]

    def get_room(self, id):
        return self.get_by_id(id)

    def create(self, title, teamId=None):
        payload = {'title': title, 'teamId': teamId}
        data = self.session.post(self.url(), json=payload)
        return self.DataClass(data)

    def update(self, title, id):
        payload = {'title': title}
        data = self.session.put(self.url(id), json=payload)
        return self.DataClass(data)
