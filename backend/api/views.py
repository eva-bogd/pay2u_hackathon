from datetime import datetime, timedelta

from django.db.models import Q, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from services.models import Subscription, Tariff, Transaction, UserTariff

from .serializers import (MySubscriptionSerializer, ServiceShortSerializer,
                          SubscriptionTariffSerializer, TariffSerializer,
                          TransactionSerializer, UserTariffSerializer)
from .utils import calculate_total_cashback, get_next_payments_data


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для подписок"""
    # http://127.0.0.1:8000/api/v1/services/
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
        (next_payment_date,
         next_payment_tariffs) = get_next_payments_data(mytariffs)
        # суммируем цену к оплате по тарифам с датой окончания
        # которую нашли выше
        payment_sum = next_payment_tariffs.aggregate(
            Sum('tariff__price')
        )['tariff__price__sum']
        response_data = {
            'next_payment_date': next_payment_date,
            'payment_sum': payment_sum,
        }
        return Response(response_data)

    @action(detail=False,
            methods=['get'],
            url_path='next_payment_details')
    def get_next_payment_details(self, request):
        """Возвращает дату и сумму следующего запланированного платежа."""
        mytariffs = self.get_queryset()
        (next_payment_date,
         next_payment_tariffs) = get_next_payments_data(mytariffs)
        serializer = MySubscriptionSerializer(
            next_payment_tariffs,
            many=True
        )
        return Response(serializer.data)

    @action(details=False,
            methods=['get'],
            url_path='payment_history')
    def get_payment_history(self, request):
        """Возвращает историю платежей."""
        mytariffs = self.get_queryset()
        mytransactions = mytariffs.transactions.filter(payment_status=1)
        serializer = TransactionSerializer(mytransactions, many=True)
        return Response(serializer.data)

    # для экрана choose_plan
    # http://127.0.0.1:8000/api/v1/services/<services_id>/
    def retrieve(self, request, pk=None):
        """Возвращает подписку и список тарифов к ней."""
        subscription_id = pk
        queryset = Subscription.objects.filter(
            id=subscription_id).prefetch_related('tariffs')
        serializer = SubscriptionTariffSerializer(queryset, many=True)
        return Response(serializer.data)


class TariffViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тарифов."""
    # получить инфу о конкретном тарифе:
    # http://127.0.0.1:8000/api/v1/tariffs/<tariff_id>/
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer

    # метод для подписки на тариф (создание тарифа пользователя)
    # http://127.0.0.1:8000/api/v1/tariffs/<tariff_id>/subscribe/
    @action(methods=['post'],
            detail=True,
            url_path='subscribe')
    def subscribe(self, request, *args, **kwargs):
        """Создает и возвращает тариф пользователя и оплату по тарифу."""
        user = request.user
        tariff = self.get_object()

        if UserTariff.objects.filter(user=user, tariff=tariff).exists():
            return Response(
                {'error': 'Вы уже подписаны на данный тариф.'},
                status=status.HTTP_400_BAD_REQUEST)

        # создаем оплату
        transaction_date = datetime.now().date()
        transaction = Transaction.objects.create(
            user_tariff=None,  # юзер тариф пока не создаем
            date=transaction_date,
            amount=tariff.price,
            payment_status=1)  # имитация успешного платежа

        # создаем тариф пользователя
        start_date = transaction_date
        end_date = start_date + timedelta(days=30 * tariff.period)
        user_tariff = UserTariff.objects.create(
            user=user,
            tariff=tariff,
            start_date=transaction_date,
            end_date=end_date)

        transaction.user_tariff = user_tariff  # привязываем оплату к тарифу
        transaction.save()
        serializer = UserTariffSerializer(user_tariff)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserTariffViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тарифов пользователя."""
    # http://127.0.0.1:8000/api/v1/usertariffs/
    # http://127.0.0.1:8000/api/v1/usertariffs/usertariffs_id/)
    serializer_class = UserTariffSerializer

    def get_queryset(self):
        user = self.request.user
        return user.user_tariffs.all()

    # метод для отключения автопродления
    # http://127.0.0.1:8000/api/v1/usertariffs/<usertariffs_id>/autorenewal_off/)
    @action(methods=['post'],
            detail=True,
            url_path='autorenewal_off')
    def autorenewal_off(self, request, *args, **kwargs):
        user_tariff_id = kwargs.get('pk')
        user_tariff = UserTariff.objects.get(id=user_tariff_id)
        user_tariff.auto_renewal = False
        user_tariff.save()
        serializer = UserTariffSerializer(user_tariff)
        return Response(serializer.data)

    # метод для включения автопродления
    # http://127.0.0.1:8000/api/v1/usertariffs/<usertariffs_id>/autorenewal_on/)
    @action(methods=['post'],
            detail=True,
            url_path='autorenewal_on')
    def autorenewal_on(self, request, *args, **kwargs):
        user_tariff_id = kwargs.get('pk')
        user_tariff = UserTariff.objects.get(id=user_tariff_id)
        user_tariff.auto_renewal = True
        user_tariff.save()
        serializer = UserTariffSerializer(user_tariff)
        return Response(serializer.data)
