from datetime import datetime

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from services.models import Subscription, Tariff

from .serializers import (MySubscriptionSerializer, ServiceShortSerializer,
                          SubscriptionShortSerializer, TariffSerializer)
from .utils import calculate_total_cashback


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для подписок"""
    queryset = Subscription.objects.all()
    serializer_class = ServiceShortSerializer

    # для экрана my_subscriptions
    @action(detail=False,
            methods=['get'],
            url_path='my_subscriptions')
    def get_my_subscriptions(self, request):
        """Возвращает активные и неактивные подписки + сумму кэшбэка."""
        now = datetime.now()
        month_start = now.replace(day=1,
                                  hour=0,
                                  minute=0,
                                  second=0,
                                  microsecond=0)
        next_month = month_start.replace(month=month_start.month + 1)
        user = request.user
        mytariffs = user.user_tariffs.all()
        active_tariffs = mytariffs.filter(end_date__gte=now)
        inactive_tariffs = mytariffs.filter(end_date__lt=now)
        # все подписки начало которых в этом месяце или
        # где есть автропрдление и конец подписки в этом месяце
        payload = mytariffs.filter(
            Q(start_date__gte=month_start)
            | (Q(auto_renewal=True) & Q(end_date__lt=next_month))
        )
        active_subscriptions = MySubscriptionSerializer(
            active_tariffs,
            many=True
        )
        inactive_subscriptions = MySubscriptionSerializer(
            inactive_tariffs,
            many=True
        )

        total_cashback = calculate_total_cashback(payload)
        response_data = {
            'active_subscriptions': active_subscriptions.data,
            'inactive_subscriptions': inactive_subscriptions.data,
            'total_cashback': total_cashback,
        }
        return Response(response_data)


class TariffViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тарифов."""
    serializer_class = TariffSerializer

    def get_queryset(self):
        queryset = Subscription.objects.get(id=self.kwargs['service_id'])
        return queryset

    # для экрана choose_plan
    @action(detail=True,
            methods=['get'])
    def get_tariffs(self, request, pk=None):
        subscription_id = pk
        queryset = Subscription.objects.filter(
            id=subscription_id).prefetch_related('tariffs')
        serializer = SubscriptionShortSerializer(queryset, many=True)
        return Response(serializer.data)

    # для экрана about_subscription
    @action(detail=True,
            methods=['get'])
    def get_tariff_detail(self, request, pk=None):
        tariff = Tariff.objects.get(id=pk)
        serializer = TariffSerializer(tariff)
        return Response(serializer.data)
