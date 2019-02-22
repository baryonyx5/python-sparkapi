"""Spark Teams Classes."""

from .spark_class import SparkDataClass, SparkAPI


class Team(SparkDataClass):
    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.name = data.pop('roomId')
        self.created = self.set_datetime(data.pop('created'))
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class Teams(SparkAPI):

    DataClass = Team

    def get_team(self, teamId):
        return self.get_by_id(id=teamId)

    def create(self, name):
        payload = {'name': name}
        data = self.session.post(self.url, payload=payload)
        return self.DataClass(data)

    def update(self, id, name):
        payload = {'name': name}
        data = self.session.put(self.url, id=id, payload=payload)
        return self.DataClass(data)