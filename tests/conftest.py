import os
import pytest
from urllib.parse import quote
import betamax
from sparkapi import SparkAPI

SPARK_TOKEN = os.environ.get('SPARK_TOKEN')
EMAIL = os.environ.get('SPARK_EMAIL')
CASSETTE_LIBRARY_DIR = '/Users/kms/git/sparkapi/tests/cassettes/'


config = betamax.Betamax.configure()
config.cassette_library_dir = CASSETTE_LIBRARY_DIR
config.default_cassette_options['record_mode'] = 'once'
config.define_cassette_placeholder('<SPARK-TOKEN>', SPARK_TOKEN)
config.define_cassette_placeholder('<SPARK-EMAIL>', EMAIL)
config.define_cassette_placeholder('<SPARK-EMAIL>', quote(EMAIL))


@pytest.fixture(scope='session', name='sp')
def sparkapi_fixture() -> SparkAPI:
    return SparkAPI(access_token=SPARK_TOKEN)


@pytest.fixture(scope='session', name='recorder')
def recorder_fixture(sp):
    recorder = betamax.Betamax(sp.session, cassette_library_dir=CASSETTE_LIBRARY_DIR)
    return recorder
