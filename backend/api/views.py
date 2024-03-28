from datetime import datetime

from django.db.models import Min, Q, Sum
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


class MySubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для подписок пользователя"""
    serializer_class = MySubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return user.user_tariffs.all()

    # для экрана my_subscriptions
    @action(detail=False,
            methods=['get'],
            url_path='cashback')
    def get_cashback(self, request):
        """Возвращает сумму кэшбэка по подпискам на текущий месяц."""
        now = datetime.now()
        month_start = now.replace(day=1,
                                  hour=0,
                                  minute=0,
                                  second=0,
                                  microsecond=0)
        next_month = month_start.replace(month=month_start.month + 1)
        mytariffs = self.get_queryset()
        # все подписки начало которых в этом месяце или
        # где есть автропрдление и конец подписки в этом месяце
        payload = mytariffs.filter(
            Q(start_date__gte=month_start)
            | (Q(auto_renewal=True) & Q(end_date__lt=next_month))
        )
        total_cashback = calculate_total_cashback(payload)
        response_data = {
            "total_cashback": total_cashback
        }
        return Response(response_data)

    @action(detail=False,
            methods=['get'],
            url_path='next_payment')
    def get_next_payment(self, request):
        """Возвращает дату и сумму следующего запланированного платежа."""
        mytariffs = self.get_queryset()
        # тарифы по которым есть автопродление
        auto_renewal_tariffs = mytariffs.filter(auto_renewal=True)
        # выбираем из них тариф с ближайшей датой окончания
        next_payment = auto_renewal_tariffs.aggregate(
            min_end_date=Min('end_date')
        )['min_end_date']
        # суммируем цену к оплате по тарифам с датой окончания
        # которую нашли выше
        payment_sum = auto_renewal_tariffs.filter(
            end_date=next_payment
        ).aggregate(
            Sum('tariff__price')
        )['tariff__price__sum']
        response_data = {
            'next_payment_date': next_payment,
            'payment_sum': payment_sum,
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
