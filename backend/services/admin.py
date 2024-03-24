from django.contrib import admin

from .models import Subscription, Tariff, Transaction, UserTariff


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin for subscriptions"""
    list_display = (
        'pk',
        'name',
    )
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    """Admin for tarrifs"""
    list_display = (
        'pk',
        'subscription',
        'name',
        'duration',
        'price',
        'cashback',
        'is_direct',
    )
    list_filter = (
        'subscription',
        'duration',
        'is_direct',
    )
    search_fields = ('name',)
    ordering = ('subscription',)


admin.site.register(UserTariff)
admin.site.register(Transaction)
