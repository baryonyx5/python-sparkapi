import os
import pytest
from sparkapi import SparkAPI

SPARK_TOKEN = os.environ.get('SPARK_TOKEN')


@pytest.fixture(name='sp')
def load_sparkapi_fixture():
    return SparkAPI(access_token=SPARK_TOKEN)
