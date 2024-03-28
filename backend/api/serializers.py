from django.db.models import Min
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from services.models import Subscription, Tariff, UserTariff
from users.models import User


class MySubscriptionSerializer(serializers.Serializer):
    name = serializers.CharField(source='tariff.subscription.name')
    logo = serializers.ImageField(source='tariff.subscription.logo')
    price = serializers.DecimalField(source='tariff.price',
                                     max_digits=10,
                                     decimal_places=2)
    cashback = serializers.DecimalField(source='tariff.cashback',
                                        max_digits=10,
                                        decimal_places=2)

    class Meta:
        model = UserTariff
        fields = ('id', 'name', 'logo', 'price', 'cashback')


class ServiceShortSerializer(serializers.ModelSerializer):
    logo = Base64ImageField()
    min_tariff_price = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'name', 'logo', 'description', 'min_tariff_price')

    def get_min_tariff_price(self, instance):
        min_price = instance.tariffs.aggregate(
            min_price=Min('price')
        )['min_price']
        return min_price


class SubscriptionSerializer(serializers.ModelSerializer):
    logo = Base64ImageField()

    class Meta:
        model = Subscription
        fields = ('id', 'name', 'logo', 'description', 'usage_policy')


class TariffListSerializer(serializers.ModelSerializer):
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
    tariffs = TariffListSerializer(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = ('id',
                  'name',
                  'logo',
                  'description',
                  'tariffs')


class TariffSerializer(serializers.ModelSerializer):
    subscription = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tariff
        fields = ('id',
                  'subscription',
                  'name',
                  'description',
                  'period',
                  'price',
                  'test_period',
                  'test_price',
                  'cashback',
                  'cashback_conditions')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name',
                  'father_name',
                  'last_name',
                  'phone_number')


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
                  'is_direct')
