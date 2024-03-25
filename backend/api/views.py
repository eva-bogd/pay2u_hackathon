from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from services.models import Subscription, Tariff

from .serializers import (SubscriptionSerializer,
                          SubscriptionShortSerializer,
                          TariffSerializer)


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    # для экрана choose_plan
    @action(detail=True,
            methods=['get'],
            url_path='tariffs')
    def get_tariffs(self, request, pk=None):
        subscription_id = pk
        queryset = Subscription.objects.filter(
            id=subscription_id).prefetch_related('tariffs')
        serializer = SubscriptionShortSerializer(queryset, many=True)
        return Response(serializer.data)

    # для экрана about_subscription
    @action(detail=True,
            methods=['get'],
            url_path='tariffs/(?P<tariff_id>\d+)')
    def get_tariff_detail(self, request, pk=None, tariff_id=None):
        tariff = Tariff.objects.get(id=tariff_id)
        serializer = TariffSerializer(tariff)
        return Response(serializer.data)
