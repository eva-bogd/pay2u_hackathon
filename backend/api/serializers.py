from datetime import datetime

from django.db.models import Max, Min
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from services.models import Subscription, Tariff, Transaction, UserTariff
from users.models import User

from .utils import calculate_cashback_amount


class MySubscriptionSerializer(serializers.Serializer):
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


class TransactionSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Subscription
        fields = ('id', 'partner_rules')


class PDpolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'personal_data_policy')


class TariffSerializer(serializers.ModelSerializer):
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
        return obj.price / obj.period


class SubscriptionTariffSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name',
                  'father_name',
                  'last_name',
                  'phone_number')


class CustomCurrentUserSerializer(serializers.Serializer):
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
