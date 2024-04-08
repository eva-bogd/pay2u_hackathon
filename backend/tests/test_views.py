from unittest.mock import patch

import api.serializers as api_s
import pytest
from api.utils import PAYMENT_SUCCESS, get_next_payments
from services.models import Subscription, Tariff, Transaction, UserTariff


@pytest.mark.django_db
def test_urls_data(subscription, tariff, authenticated_client, user,
                   transactions):
    urls_data = {
        'services/': api_s.ServiceSerializer(
            Subscription.objects.all(), many=True
        ).data,
        f'services/{subscription.id}/':
            api_s.SubscriptionTariffSerializer(subscription).data,
        f'services/{subscription.id}/partner_rules/':
            api_s.PartnerRulesSerializer(subscription).data,
        f'services/{subscription.id}/personal_data_policy/':
            api_s.PDpolicySerializer(subscription).data,
        'tariffs/': api_s.TariffSerializer(
            Tariff.objects.all(), many=True
        ).data,
        f'tariffs/{tariff.id}/': api_s.TariffSerializer(tariff).data,
        'my_subscriptions/cashback/':
            api_s.TotalCashbackSerializer(user).data,
        'my_subscriptions/next_payment/':
            api_s.NextPaymentSerializer(user).data,
        'my_subscriptions/next_payment_details/':
            api_s.MySubscriptionSerializer(
                get_next_payments(user.user_tariffs.all()),
                many=True,
        ).data,
        'my_subscriptions/payment_history/':
            api_s.TransactionSerializer(
                Transaction.objects.filter(
                    user_tariff__user=user,
                    payment_status=PAYMENT_SUCCESS),
                many=True,
        ).data,
    }
    for url, data in urls_data.items():
        response = authenticated_client.get(f'/api/v1/{url}')
        assert response.data == data


@pytest.mark.django_db
def test_mysubscriptions_list(user, authenticated_client,
                              user_tariff, another_user_tariff):
    """
    Проверяет, что my_subscriptions/
    отображаются данные только по подпискам юзера.
    """
    response = authenticated_client.get('/api/v1/my_subscriptions/')
    assert response.data == api_s.MySubscriptionSerializer(
        user.user_tariffs.all(), many=True
    ).data
    assert response.data != api_s.MySubscriptionSerializer(
        UserTariff.objects.all(), many=True
    ).data


@pytest.mark.django_db
def test_subscribe_to_tariff_success(tariff, user, authenticated_client):
    """
    Проверяет успешную подписку на тариф (в случае, когда оплата прошла).
    """
    usertariff_before = UserTariff.objects.filter(user=user).count()
    transaction_before = Transaction.objects.all().count()
    with patch('api.views.simulate_payment_status', return_value=1):
        response = authenticated_client.post(
            f'/api/v1/tariffs/{tariff.id}/subscribe/'
        )
    assert response.status_code == 201
    assert UserTariff.objects.filter(
        user=user).count() == usertariff_before + 1
    assert Transaction.objects.all().count() == transaction_before + 1


@pytest.mark.django_db
def test_subscribe_to_tariff_failure(tariff, user, authenticated_client):
    """
    Проверяет неудачную подписку на тариф (в случае, когда оплата не прошла).
    """

    usertariff_before = UserTariff.objects.filter(user=user).count()
    transaction_before = Transaction.objects.all().count()
    with patch('api.views.simulate_payment_status', return_value=0):
        response = authenticated_client.post(
            f'/api/v1/tariffs/{tariff.id}/subscribe/'
        )
    assert response.status_code == 400
    assert UserTariff.objects.filter(user=user).count() == usertariff_before
    assert Transaction.objects.all().count() == transaction_before + 1
