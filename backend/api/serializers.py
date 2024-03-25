from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from services.models import Subscription, Tariff


class SubscriptionSerializer(serializers.ModelSerializer):
    logo = Base64ImageField()

    class Meta:
        model = Subscription
        fields = ('id', 'name', 'logo', 'description', 'usage_policy')


class TariffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ('id', 'name', 'duration', 'price',
                  'test_period', 'test_price', 'cashback')


class SubscriptionShortSerializer(serializers.ModelSerializer):
    logo = Base64ImageField()
    tariffs = TariffListSerializer(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'logo', 'description', 'tariffs')


class TariffSerializer(serializers.ModelSerializer):
    subscription = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tariff
        fields = ('id', 'subscription', 'name', 'description',
                  'duration', 'price', 'test_period', 'test_price',
                  'cashback', 'cashback_conditions')
