import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .test_factories import (UserFactory,
                             SubscriptionFactory,
                             TariffFactory,
                             UserTariffFactory,
                             TransactionFactory)


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
def subscription():
    subscription = SubscriptionFactory()
    TariffFactory.create_batch(2, subscription=subscription)
    return subscription


@pytest.fixture
def tariff():
    subscription = SubscriptionFactory()
    tariff = TariffFactory(subscription=subscription)
    return tariff


@pytest.fixture
def user_tariff(user, tariff):
    return UserTariffFactory(user=user, tariff=tariff)


@pytest.fixture
def transaction(user_tariff):
    return TransactionFactory(user_tariff=user_tariff)
