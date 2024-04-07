import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from tests.test_factories import UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def authenticated_client(user):
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.fixture
def guest_client():
    return APIClient()


@pytest.fixture
def another_user():
    return UserFactory()
