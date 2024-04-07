from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_urls_authenticated_user(subscription, tariff,
                                 user_tariff, authenticated_client):
    urls_status = {
        'services/': HTTPStatus.OK,
        f'services/{subscription.id}/': HTTPStatus.OK,
        f'services/{subscription.id}/partner_rules/': HTTPStatus.OK,
        f'services/{subscription.id}/personal_data_policy/': HTTPStatus.OK,
        'tariffs/': HTTPStatus.OK,
        f'tariffs/{tariff.id}/': HTTPStatus.OK,
        f'tariffs/{tariff.id}/subscribe/': HTTPStatus.METHOD_NOT_ALLOWED,
        'my_subscriptions/': HTTPStatus.OK,
        'my_subscriptions/cashback/': HTTPStatus.OK,
        'my_subscriptions/next_payment/': HTTPStatus.OK,
        'my_subscriptions/next_payment_details/': HTTPStatus.OK,
        'my_subscriptions/payment_history/': HTTPStatus.OK,
        f'my_subscriptions/{user_tariff.id}/autorenewal_on/':
            HTTPStatus.METHOD_NOT_ALLOWED,
        f'my_subscriptions/{user_tariff.id}/autorenewal_off/':
            HTTPStatus.METHOD_NOT_ALLOWED,
        'unexisting_page/': HTTPStatus.NOT_FOUND,
    }
    for url, status in urls_status.items():
        response = authenticated_client.get(f'/api/v1/{url}')
        assert response.status_code == status


@pytest.mark.django_db
def test_urls_guest_user(subscription, tariff, user_tariff, guest_client):
    urls = (
        'services/',
        f'services/{subscription.id}/',
        f'services/{subscription.id}/partner_rules/',
        f'services/{subscription.id}/personal_data_policy/',
        'tariffs/',
        f'tariffs/{tariff.id}/',
        f'tariffs/{tariff.id}/subscribe/',
        'my_subscriptions/',
        'my_subscriptions/cashback/',
        'my_subscriptions/next_payment/',
        'my_subscriptions/next_payment_details/',
        'my_subscriptions/payment_history/',
        f'my_subscriptions/{user_tariff.id}/autorenewal_on/',
        f'my_subscriptions/{user_tariff.id}/autorenewal_off/',
    )
    for url in urls:
        response = guest_client.get(f'/api/v1/{url}')
        assert response.status_code == HTTPStatus.UNAUTHORIZED
