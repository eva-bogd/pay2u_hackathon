from decimal import Decimal

from django.db.models import Min, QuerySet
from services.models import UserTariff


def calculate_cashback_amount(instance: UserTariff) -> Decimal:
    """Считает кэшбэка в руб."""
    cashback_amount = Decimal(0)
    # Кэшбэк в %
    cashback_percentage = instance.tariff.cashback
    if cashback_percentage:
        # Цена в рублях
        price = instance.tariff.price
        # Кэшбэк в рублях
        cashback_amount = price * cashback_percentage / 100
    return cashback_amount


def calculate_total_cashback(payload: QuerySet[UserTariff]) -> Decimal:
    """Считает сумму кэшбэка."""
    total_cashback = Decimal(0)
    for user_tariff in payload:
        cashback_amount = calculate_cashback_amount(user_tariff)
        total_cashback += cashback_amount
    return round(total_cashback, 2)


def get_next_payments_data(
    data: QuerySet[UserTariff]
) -> tuple[str, QuerySet[UserTariff]]:
    """Возвращает следующую дату платежа и перечень тарифов к оплате."""
    # тарифы по которым есть автопродление
    auto_renewal_tariffs = data.filter(auto_renewal=True)
    # выбираем из них тариф с ближайшей датой окончания
    next_payment_date = auto_renewal_tariffs.aggregate(
        min_end_date=Min('end_date')
    )['min_end_date']
    # суммируем цену к оплате по тарифам с датой окончания
    # которую нашли выше
    queryset = auto_renewal_tariffs.filter(
        end_date=next_payment_date
    )
    return next_payment_date, queryset