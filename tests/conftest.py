import os

import pytest
from django.db import connection

DB_SCHEMA = os.getenv('DB_SCHEMA')

pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_data',
]

@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        pass
