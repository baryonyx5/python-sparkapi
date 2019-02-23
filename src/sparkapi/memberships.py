"""Spark Membership Class. """

from .base import BaseObject, BaseAPI


class Membership(BaseObject):
    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.roomId = data.pop('roomId')
        self.personId = data.pop('personId')
        self.personEmail = data.pop('personEmail')
        self.personDisplayName = data.pop('personDisplayName', '')
        self.personOrgId = data.pop('personOrgId', '')
        self.isModerator = self.set_bool(data.pop('isModerator'))
        self.isMonitor = self.set_bool(data.pop('isMonitor'))
        self.created = self.set_datetime(data.pop('created'))
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class Memberships(BaseAPI):
    DataClass = Membership
    uri = 'memberships'

    def get_by_room(self, roomId, max=None):
        return self.list(roomId=roomId, max=max)

    def get_by_person(self, roomId, personId=None, personEmail=None):
        params = self._id_or_email(personId=personId, personEmail=personEmail)
        params['roomId'] = roomId
        return self.list(**params)

    def get_membership(self, id):
        return self.get_by_id(id)

    def create(self, roomId, personId=None, personEmail=None, isModerator=False):
        payload = self._id_or_email(personId=personId, personEmail=personEmail)
        payload['roomId'] = roomId
        payload['isModerator'] = isModerator
        data = self.session.post(self.url(), payload=payload)
        return self.DataClass(data)

    def update(self, id, isModerator):
        payload = {'isModerator': isModerator}
        data = self.session.put(self.url(id), payload=payload)
        return self.DataClass(data)
