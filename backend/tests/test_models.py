import pytest
from services.models import Subscription, Tariff, Transaction, UserTariff
from test_factories import (SubscriptionFactory, TariffFactory,
                            TransactionFactory, UserFactory, UserTariffFactory,
                            TransactionFactory)
from users.models import User


@pytest.mark.django_db
def test_user_factory():
    user = UserFactory()
    assert isinstance(user, User)
    assert user.email
    assert user.first_name
    assert user.last_name
    assert user.father_name
    assert user.phone_number


@pytest.mark.django_db
def test_subscription_factory():
    subscription = SubscriptionFactory()
    assert isinstance(subscription, Subscription)
    assert subscription.name
    assert subscription.description
    assert subscription.usage_policy


@pytest.mark.django_db
def test_tariff_factory():
    tariff = TariffFactory()
    assert isinstance(tariff, Tariff)
    assert tariff.name
    assert tariff.subscription
    assert tariff.description
    assert tariff.duration
    assert tariff.price
    assert tariff.test_period
    assert tariff.test_price
    assert tariff.cashback
    assert tariff.cashback_conditions
    assert isinstance(tariff.is_direct, bool)


@pytest.mark.django_db
def test_user_tariff_factory():
    user_tariff = UserTariffFactory()
    assert isinstance(user_tariff, UserTariff)
    assert user_tariff.user
    assert user_tariff.tariff
    assert user_tariff.start_date
    assert user_tariff.end_date
    assert type(user_tariff.auto_renewal) is bool


@pytest.mark.django_db
def test_transaction_factory():
    transaction = TransactionFactory()
    assert isinstance(transaction, Transaction)
    assert transaction.user_tariff
    assert transaction.date
    assert transaction.amount
    assert transaction.payment_status in [0, 1, 2]
