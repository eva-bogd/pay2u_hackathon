import pytest
from services.models import Subscription, Tariff, Transaction, UserTariff
from .test_factories import (SubscriptionFactory, TariffFactory,
                             TransactionFactory, UserFactory,
                             UserTariffFactory)
from users.models import User


@pytest.mark.django_db
def test_user_factory():
    user = UserFactory()
    assert isinstance(user, User)
    fields_to_check = ['email', 'first_name', 'last_name', 'father_name',
                       'phone_number']
    for field in fields_to_check:
        assert getattr(user, field)


@pytest.mark.django_db
def test_subscription_factory():
    subscription = SubscriptionFactory()
    assert isinstance(subscription, Subscription)
    fields_to_check = ['name', 'description', 'partner_rules',
                       'personal_data_policy']
    for field in fields_to_check:
        assert getattr(subscription, field)


@pytest.mark.django_db
def test_tariff_factory():
    tariff = TariffFactory()
    assert isinstance(tariff, Tariff)
    fields_to_check = ['name', 'subscription', 'description',
                       'period', 'price', 'test_period', 'test_price',
                       'cashback', 'cashback_conditions']
    for field in fields_to_check:
        assert getattr(tariff, field)


@pytest.mark.django_db
def test_user_tariff_factory():
    user_tariff = UserTariffFactory()
    assert isinstance(user_tariff, UserTariff)
    fields_to_check = ['user', 'tariff', 'start_date', 'end_date',
                       'promo_code', 'promo_code_period']
    for field in fields_to_check:
        assert getattr(user_tariff, field)
    assert isinstance(user_tariff.is_direct, bool)
    assert isinstance(user_tariff.auto_renewal, bool)


@pytest.mark.django_db
def test_transaction_factory():
    transaction = TransactionFactory()
    assert isinstance(transaction, Transaction)
    fields_to_check = ['user_tariff', 'date', 'amount', 'cashback',
                       'payment_status']
    for field in fields_to_check:
        assert getattr(transaction, field)
