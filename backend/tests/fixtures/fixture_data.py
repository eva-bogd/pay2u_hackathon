import pytest
from tests.test_factories import (SubscriptionFactory, TariffFactory,
                                  TransactionFactory, UserTariffFactory)


@pytest.fixture
def subscription():
    subscription = SubscriptionFactory()
    TariffFactory.create_batch(2, subscription=subscription)
    return subscription


@pytest.fixture
def tariff(subscription):
    tariff = TariffFactory(subscription=subscription)
    return tariff


@pytest.fixture
def user_tariff(user, tariff):
    return UserTariffFactory(user=user, tariff=tariff)


@pytest.fixture
def transaction(user_tariff):
    return TransactionFactory(user_tariff=user_tariff)


@pytest.fixture
def user_tariffs(user):
    return UserTariffFactory.create_batch(100, user=user)


@pytest.fixture
def another_user_tariff(another_user):
    return UserTariffFactory.create_batch(10, user=another_user)


@pytest.fixture
def transactions(user_tariffs):
    return [
        TransactionFactory(
            user_tariff=user_tariff
        ) for user_tariff in user_tariffs
    ]
