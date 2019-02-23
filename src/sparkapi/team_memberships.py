"""Spark Team Membership Classes."""

from .base import BaseObject, BaseAPI


class TeamMembership(BaseObject):
    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.teamId = data.pop('teamId')
        self.personId = data.pop('personId')
        self.personEmail = data.pop('personEmail')
        self.personDisplayName = data.pop('personDisplayName', '')
        self.personOrgId = data.pop('personOrgId', '')
        self.isModerator = self.set_bool(data.pop('isModerator'))
        self.created = self.set_datetime(data.pop('created'))
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class TeamMemberships(BaseAPI):
    DataClass = TeamMembership
    uri = 'team/memberships'

    def get_team_membership(self, id):
        return self.get_by_id(id)

    def create(self, teamId, personId=None, personEmail=None, isModerator=False):
        payload = self._id_or_email(personId=personId, personEmail=personEmail)
        payload['teamId'] = teamId
        payload['isModerator'] = isModerator
        data = self.session.post(self.url(), payload=payload)
        return self.DataClass(data)

    def update(self, id, isModerator):
        payload = {'isModerator': isModerator}
        data = self.session.put(self.url(id), payload=payload)
        return self.DataClass(data)
