import pytest


@pytest.fixture
def password():
    return '1234567'


@pytest.fixture
def user(django_user_model, password):
    return django_user_model.objects.create_user(
        username='TestUser',
        password=password
    )