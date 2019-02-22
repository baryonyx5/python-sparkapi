"""Spark Organization Classes."""

from .spark_class import SparkDataClass, SparkAPI


class Organization(SparkDataClass):

    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.displayName = data.pop('displayName', '')
        self.created = self.set_datetime(data.pop('created'))
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class Organizations(SparkAPI):

    DataClass = Organization

    def delete(self, id):
        """Not Implemented"""
        pass
