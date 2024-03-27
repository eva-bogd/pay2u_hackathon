from decimal import Decimal

from django.db.models import QuerySet
from services.models import UserTariff


def calculate_total_cashback(payload: QuerySet[UserTariff]) -> Decimal:
    """Считает сумму кэшбэка."""
    total_cashback = Decimal(0)
    for tariff in payload:
        # Цена в рублях
        price = tariff.tariff.price
        # Кэшбэк в %
        cashback_percentage = tariff.tariff.cashback
        if cashback_percentage:
            cashback_amount = price * cashback_percentage / 100
            total_cashback += round(cashback_amount, 2)
    return total_cashback
