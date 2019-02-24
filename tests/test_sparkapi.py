import datetime
import pytest
import betamax
from sparkapi import SparkAPI
from sparkapi import exc
from sparkapi.people import Person
from sparkapi.rooms import Room
from .conftest import SPARK_TOKEN, CASSETTE_LIBRARY_DIR

# config = Betamax.configure()
# config.cassette_library_dir = CASSETTE_LIBRARY_DIR
# config.define_cassette_placeholder('<SPARK-TOKEN>', TOKEN)


def test_api_init(sp, recorder):
    """
    Given a valid access token
    When passing it to the SparkAPI constructor
    Then a SparkAPI instance is returned with the access_token attribute set
     and People.me API request is successful
    """

    with recorder.use_cassette('test_api_init'):
        assert isinstance(sp, SparkAPI)
        assert sp.access_token == SPARK_TOKEN
        assert isinstance(sp.me, Person)


def test_api_init_failure():
    """
    Given an invalid access token
    When passing it to the SparkAPI constructor
    Then an API request raises a HTTPError exception
    """
    spbad = SparkAPI('notavalidtoken')
    recorder = betamax.Betamax(spbad.session, cassette_library_dir=CASSETTE_LIBRARY_DIR)
    with recorder.use_cassette('test_api_init_failure'):
        with pytest.raises(exc.HTTPError) as ex:
            spbad.me()
        assert ex.value.response.status_code == 401
        assert ex.value.response.reason == 'Unauthorized'


def test_people_me(sp, recorder):
    with recorder.use_cassette('test_people_me'):
        me = sp.people.me()
        assert isinstance(sp.me, Person)
        assert me.id
        assert me.email == 'baryonyx5@gmail.com'
        assert isinstance(me.created, datetime.datetime)


def test_people_get_by_id(sp, recorder):
    """
    Given a SparkAPI instance and an id for an existing Spark user
    When calling get_by_id
    Then a Person object is returned and the id attribute matches
    """
    me = sp.people.me()
    with recorder.use_cassette('test_people_get_by_id'):
        person = sp.people.get_by_id(me.id)
        assert isinstance(person, Person)
        assert person.id == me.id


def test_people_get_by_email(sp, recorder):
    """
    Given a SparkAPI instance and an email address for an existing Spark user
    When calling get_by_email t
    Then a list containing a single Person object is returned and th email
     attribute matches
    """
    email = 'kris.seraphine@cdw.com'
    with recorder.use_cassette('test_people_get_by_email'):
        person = sp.people.get_by_email(email)
        assert isinstance(person[0], Person)
        assert person[0].email == email

def test_room_list(sp, recorder):
    """
    Given a SparkAPI instance
    When calling the Room.list method
    Then a list of Room instances is returned with attributes
     set to the expected types
    """
    with recorder.use_cassette('test_room_list'):
        rooms = sp.rooms.list()
        assert isinstance(rooms[0], Room)
        assert rooms[0].id
        assert rooms[0].type in ['group', 'direct']
