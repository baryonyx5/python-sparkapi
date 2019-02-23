"""Spark License Classes."""

from .base import BaseObject, BaseAPI


class License(BaseObject):

    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.name = data.pop('name')
        self.totalUnits = data.pop('totalUnits')
        self.consumedUnits = data.pop('consumedUnits')
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class Licenses(BaseAPI):
    DataClass = License
    uri = 'licenses'

    def get_License(self, id):
        return self.get_by_id(id)

    def delete(self, id):
        raise NotImplementedError
