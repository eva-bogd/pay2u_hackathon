from datetime import datetime
from decimal import Decimal

from django.db.models import Max, Min, Q, Sum
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from services.models import Subscription, Tariff, Transaction, UserTariff
from users.models import User

from .utils import (calculate_cashback_amount, get_next_payments,
                    get_next_payments_date)


class MySubscriptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='tariff.subscription.name')
    logo = serializers.ImageField(source='tariff.subscription.logo')
    price = serializers.DecimalField(source='tariff.price',
                                     max_digits=10,
                                     decimal_places=2)
    cashback = serializers.DecimalField(source='tariff.cashback',
                                        max_digits=10,
                                        decimal_places=2)
    is_active = serializers.SerializerMethodField()
    cashback_rub = serializers.SerializerMethodField()

    class Meta:
        model = UserTariff
        fields = ('id', 'name', 'logo', 'price', 'cashback',
                  'is_active', 'is_direct', 'end_date', 'cashback_rub')

    def get_is_active(self, instance):
        now = datetime.now().date()
        return instance.end_date >= now

    def get_cashback_rub(self, instance):
        return calculate_cashback_amount(instance)


class TotalCashbackSerializer(serializers.Serializer):
    """Сериализатор для вывода суммарного кэшбека за месяц."""
    total_cashback = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('total_cashback',)

    def get_total_cashback(self, instance):
        user = instance
        now = datetime.now().date()
        month_start = now.replace(day=1)
        next_month = month_start.replace(month=month_start.month + 1)
        # все подписки начало которых в этом месяце или
        # где есть автропрдление и конец подписки в этом месяце
        payload = user.user_tariffs.filter(
            Q(start_date__gte=month_start)
            | (Q(auto_renewal=True) & Q(end_date__lt=next_month))
        )
        total_cashback = Decimal(0)
        for user_tariff in payload:
            cashback_amount = calculate_cashback_amount(user_tariff)
            total_cashback += cashback_amount
        return round(total_cashback, 2)


class NextPaymentSerializer(serializers.Serializer):
    """Сериализатор для вывода следующей даты оплаты и суммы."""
    next_payment_date = serializers.SerializerMethodField()
    payment_sum = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('next_payment_date', 'payment_sum')

    def get_next_payment_date(self, instance):
        """Возвращает дату и сумму следующего запланированного платежа."""
        mytariffs = instance.user_tariffs.all()
        next_payment_date = get_next_payments_date(mytariffs)
        return next_payment_date

    def get_payment_sum(self, instance):
        """Возвращает дату и сумму следующего запланированного платежа."""
        mytariffs = instance.user_tariffs.all()
        next_payments = get_next_payments(mytariffs)
        # суммируем цену к оплате по тарифам с датой окончания
        # которую нашли выше
        payment_sum = next_payments.aggregate(
            Sum('tariff__price')
        )['tariff__price__sum']
        return payment_sum


class TransactionSerializer(serializers.ModelSerializer):
    """Сериализатор для транзакций."""
    name = serializers.CharField(
        source='user_tariff.tariff.subscription.name'
    )
    logo = serializers.ImageField(
        source='user_tariff.tariff.subscription.logo'
    )
    cashback_rub = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'name', 'logo', 'cashback_rub')

    def get_cashback_rub(self, instance):
        user_tariff = instance.user_tariff
        return calculate_cashback_amount(user_tariff)


class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для онлайн сервисов."""
    logo = Base64ImageField()
    min_tariff_price = serializers.SerializerMethodField()
    cashback = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'name', 'logo', 'description',
                  'cashback', 'min_tariff_price')

    def get_min_tariff_price(self, instance):
        min_price = instance.tariffs.aggregate(
            min_price=Min('price')
        )['min_price']
        return min_price

    def get_cashback(self, instance):
        max_cashback = instance.tariffs.aggregate(
            max_cashback=Max('cashback')
        )['max_cashback']
        return max_cashback


class PartnerRulesSerializer(serializers.ModelSerializer):
    """Сериализатор для правил партнера."""

    class Meta:
        model = Subscription
        fields = ('id', 'partner_rules')


class PDpolicySerializer(serializers.ModelSerializer):
    """Сериализатор для политики обработки персональных данных."""

    class Meta:
        model = Subscription
        fields = ('id', 'personal_data_policy')


class TariffSerializer(serializers.ModelSerializer):
    """Сериализатор для тарифа."""
    period = serializers.SerializerMethodField()
    test_period = serializers.SerializerMethodField()
    month_price = serializers.SerializerMethodField()
    logo = Base64ImageField(source='subscription.logo', read_only=True)

    class Meta:
        model = Tariff
        fields = ('id',
                  'logo',
                  'name',
                  'description',
                  'period',
                  'price',
                  'test_period',
                  'test_price',
                  'cashback',
                  'cashback_conditions',
                  'month_price',)

    def get_period(self, obj):
        return obj.get_period_display()

    def get_test_period(self, obj):
        return obj.get_test_period_display()

    def get_month_price(self, obj):
        return round((obj.price / obj.period), 2)


class SubscriptionTariffSerializer(serializers.ModelSerializer):
    """Сериализатор для тарифов сервиса."""

    logo = Base64ImageField()
    tariffs = TariffSerializer(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = ('id',
                  'name',
                  'logo',
                  'description',
                  'tariffs')


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомного юзера."""

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name',
                  'father_name',
                  'last_name',
                  'phone_number')


class CustomCurrentUserSerializer(serializers.Serializer):
    """Сериализатор для вывода текущего юзера."""

    id = serializers.IntegerField()
    full_name = serializers.CharField()
    phone_number = serializers.CharField()

    def to_representation(self, instance):
        full_name = (f'{instance.last_name} '
                     f'{instance.first_name} '
                     f'{instance.father_name}')
        return {
            'id': instance.id,
            'full_name': full_name,
            'phone_number': instance.phone_number
        }


class UserTariffSerializer(serializers.ModelSerializer):
    """Сериализатор для связи юзера и тарифа."""

    tariff = serializers.StringRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserTariff
        fields = ('id',
                  'user',
                  'tariff',
                  'start_date',
                  'end_date',
                  'auto_renewal',
                  'is_direct',
                  'promo_code',
                  'promo_code_period')
