from sparkapi import SparkAPI
from sparkapi.people import Person
from .conftest import SPARK_TOKEN


def test_api_init(sp):
    """
    Given a valid access token
    When passing it to the SparkAPI constructor
    Then a SparkAPI instance is returned with the access_token attribute set
    """
    assert isinstance(sp, SparkAPI)
    assert sp.access_token == SPARK_TOKEN


def test_api_load_me():
    """
    Given a valid access token
    When passing it to the SparkAPI constructor with load_me=True
    Then the me attribute is set to a Person instance
    """
    sp = SparkAPI(access_token=SPARK_TOKEN, load_me=True)
    assert isinstance(sp.me, Person)


