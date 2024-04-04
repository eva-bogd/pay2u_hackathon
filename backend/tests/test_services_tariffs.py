import pytest
from unittest.mock import patch

from services.models import UserTariff, Transaction
from api.serializers import (ServiceSerializer,
                             SubscriptionTariffSerializer,
                             PartnerRulesSerializer,
                             PDpolicySerializer,
                             TariffSerializer)
from .fixture import user, authenticated_client, subscription, tariff


@pytest.mark.django_db
def test_subscription_list(subscription, authenticated_client):
    """
    Проверяет, что список подписок возвращается корректно по нужному эндоинту.
    """
    subscription = subscription
    response = authenticated_client.get('/api/v1/services/')
    assert response.status_code == 200
    assert response.data == ServiceSerializer([subscription], many=True).data


@pytest.mark.django_db
def test_subscription_retrieve(subscription, authenticated_client):
    """
    Проверяет, что подписка c тарифами к ней возвращается корректно
    по заданному ID и нужному эндоинту.
    """
    subscription = subscription
    response = authenticated_client.get(f'/api/v1/services/{subscription.id}/')
    assert response.status_code == 200
    assert response.data == SubscriptionTariffSerializer(
        [subscription], many=True).data


@pytest.mark.django_db
def test_get_partner_rules(subscription, authenticated_client):
    """
    Проверяет, что правила партнера
    возвращаются корректно для заданной подписки.
    """
    subscription = subscription
    response = authenticated_client.get(
        f'/api/v1/services/{subscription.id}/partner_rules/')
    assert response.status_code == 200
    assert response.data == PartnerRulesSerializer(
        {'partner_rules': subscription.partner_rules}).data


@pytest.mark.django_db
def get_personal_data_policy(subscription, authenticated_client):
    """
    Проверяет, что политика обработки персональных данных
    возвращается корректно для заданной подписки.
    """
    subscription = subscription
    response = authenticated_client.get(
        f'/api/v1/services/{subscription.id}/personal_data_policy/')
    assert response.status_code == 200
    assert response.data == PDpolicySerializer(
        {'personal_data_policy': subscription.personal_data_policy}).data


@pytest.mark.django_db
def test_tariff_list(tariff, authenticated_client):
    """
    Проверяет, что список тарифов возвращается корректно по нужному эндоинту.
    """
    tariff = tariff
    response = authenticated_client.get('/api/v1/tariffs/')
    assert response.status_code == 200
    assert response.data == TariffSerializer([tariff], many=True).data


@pytest.mark.django_db
def test_tariff_retrieve(tariff, authenticated_client):
    """
    Проверяет, что тариф возвращается корректно по заданному ID
    и нужному эндпоинту.
    """
    tariff = tariff
    response = authenticated_client.get(f'/api/v1/tariffs/{tariff.id}/')
    assert response.status_code == 200
    assert response.data == TariffSerializer(tariff).data


@pytest.mark.django_db
def test_subscribe_to_tariff_success(tariff, user, authenticated_client):
    """
    Проверяет успешную подписку на тариф (в случае, когда оплата прошла).
    """
    tariff = tariff
    user = user
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
    tariff = tariff
    user = user
    usertariff_before = UserTariff.objects.filter(user=user).count()
    transaction_before = Transaction.objects.all().count()
    with patch('api.views.simulate_payment_status', return_value=0):
        response = authenticated_client.post(
            f'/api/v1/tariffs/{tariff.id}/subscribe/'
        )
    assert response.status_code == 400
    assert UserTariff.objects.filter(user=user).count() == usertariff_before
    assert Transaction.objects.all().count() == transaction_before + 1
