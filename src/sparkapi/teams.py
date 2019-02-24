"""Spark Teams Classes."""

from .base import BaseObject, BaseAPI


class Team(BaseObject):
    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.name = data.pop('roomId')
        self.created = self.set_datetime(data.pop('created'))
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class Teams(BaseAPI):
    DataClass = Team
    uri = 'teams'

    def get_team(self, teamId):
        return self.get_by_id(id=teamId)

    def create(self, name):
        payload = {'name': name}
        data = self.session.post(self.url(), json=payload)
        return self.DataClass(data)

    def update(self, id, name):
        payload = {'name': name}
        data = self.session.put(self.url(id), json=payload)
        return self.DataClass(data)
