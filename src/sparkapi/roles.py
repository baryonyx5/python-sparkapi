"""Spark Roles Classes."""

from .base import BaseObject, BaseAPI


class Role(BaseObject):

    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.name = data.pop('name')
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class Roles(BaseAPI):
    DataClass = Role
    uri = 'roles'

    def get_role(self, id):
        return self.get_by_id(id)

    def delete(self, id):
        raise NotImplementedError
