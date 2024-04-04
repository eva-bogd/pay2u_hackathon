import pytest
from services.models import Subscription, Tariff, Transaction, UserTariff
from users.models import User
from .fixture import user, subscription, tariff, user_tariff, transaction


@pytest.mark.django_db
def test_user(user):
    assert isinstance(user, User)
    fields_to_check = ['email', 'first_name', 'last_name', 'father_name',
                       'phone_number']
    for field in fields_to_check:
        assert getattr(user, field)


@pytest.mark.django_db
def test_subscription(subscription):
    assert isinstance(subscription, Subscription)
    fields_to_check = ['name', 'description', 'partner_rules',
                       'personal_data_policy']
    for field in fields_to_check:
        assert getattr(subscription, field)


@pytest.mark.django_db
def test_tariff(tariff):
    assert isinstance(tariff, Tariff)
    fields_to_check = ['name', 'subscription', 'description',
                       'period', 'price', 'test_period', 'test_price',
                       'cashback', 'cashback_conditions']
    for field in fields_to_check:
        assert getattr(tariff, field)


@pytest.mark.django_db
def test_user_tariff(user_tariff):
    assert isinstance(user_tariff, UserTariff)
    fields_to_check = ['user', 'tariff', 'start_date', 'end_date',
                       'promo_code', 'promo_code_period']
    for field in fields_to_check:
        assert getattr(user_tariff, field)
    assert isinstance(user_tariff.is_direct, bool)
    assert isinstance(user_tariff.auto_renewal, bool)


@pytest.mark.django_db
def test_transaction(transaction):
    assert isinstance(transaction, Transaction)
    fields_to_check = ['user_tariff', 'date', 'amount', 'cashback']
    for field in fields_to_check:
        assert getattr(transaction, field)
    assert transaction.payment_status in [0, 1]
