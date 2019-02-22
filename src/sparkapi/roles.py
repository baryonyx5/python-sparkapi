"""Spark Roles Classes."""

from .spark_class import SparkDataClass, SparkAPI


class Role(SparkDataClass):

    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.name = data.pop('name')
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class Roles(SparkAPI):

    DataClass = Role

    def get_role(self, id):
        return self.get_by_id(id)

    def delete(self, id):
        """Not Implemented"""
        pass
