from api.serializers import (PartnerRulesSerializer, PDpolicySerializer,
                             ServiceSerializer, SubscriptionTariffSerializer)
from api.views import SubscriptionViewSet
from rest_framework.authtoken.models import Token
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)
from services.models import Subscription

from .test_factories import SubscriptionFactory, TariffFactory, UserFactory


class TestSubscriptionViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.subscription = SubscriptionFactory()
        self.subscription.save()
        self.tariffs = TariffFactory.create_batch(
            3, subscription=self.subscription)

    def test_list(self):
        factory = APIRequestFactory()
        view = SubscriptionViewSet.as_view({'get': 'list'})
        request = factory.get('/api/v1/services/')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        expected_data = ServiceSerializer(
            Subscription.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_retrieve(self):
        factory = APIRequestFactory()
        view = SubscriptionViewSet.as_view({'get': 'retrieve'})
        request = factory.get(f'/api/v1/services/{self.subscription.id}/')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.subscription.id)
        self.assertEqual(response.status_code, 200)
        expected_data = SubscriptionTariffSerializer(self.subscription).data
        self.assertEqual(response.data[0], expected_data)

    def test_get_partner_rules(self):
        factory = APIRequestFactory()
        view = SubscriptionViewSet.as_view({'get': 'get_partner_rules'})
        request = factory.get(
            f'/api/v1/services/{self.subscription.id}/partner_rules/')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.subscription.id)
        self.assertEqual(response.status_code, 200)
        expected_data = PartnerRulesSerializer(
            {'partner_rules': self.subscription.partner_rules}).data
        self.assertEqual(response.data, expected_data)

    def test_get_personal_data_policy(self):
        factory = APIRequestFactory()
        view = SubscriptionViewSet.as_view({'get': 'get_personal_data_policy'})
        request = factory.get(
            f'/api/v1/services/{self.subscription.id}/personal_data_policy/')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.subscription.id)
        self.assertEqual(response.status_code, 200)
        expected_data = PDpolicySerializer(
            {'personal_data_policy':
             self.subscription.personal_data_policy}
        ).data
        self.assertEqual(response.data, expected_data)
