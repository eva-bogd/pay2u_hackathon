import random
import string
from decimal import Decimal

from django.db.models import Min, QuerySet
from services.models import UserTariff

PAYMENT_DENIED = 0
PAYMENT_SUCCESS = 1


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


def get_next_payments_date(data: QuerySet[UserTariff]) -> str:
    """Возвращает следующую дату платежа и перечень тарифов к оплате."""
    # тарифы по которым есть автопродление
    auto_renewal_tariffs = data.filter(auto_renewal=True)
    # выбираем из них тариф с ближайшей датой окончания
    next_payment_date = auto_renewal_tariffs.aggregate(
        min_end_date=Min('end_date')
    )['min_end_date']
    return next_payment_date


def get_next_payments(data: QuerySet[UserTariff]) -> QuerySet[UserTariff]:
    """Возвращает перечень тарифов к оплате на следующую дату платежа."""
    # тарифы по которым есть автопродление
    auto_renewal_tariffs = data.filter(auto_renewal=True)
    next_payment_date = get_next_payments_date(data)
    # суммируем цену к оплате по тарифам с датой окончания
    # которую нашли выше
    queryset = auto_renewal_tariffs.filter(
        end_date=next_payment_date
    )
    return queryset


def simulate_payment_status():
    """Возвращает рандомный статус платежа (имитация ответа банка)."""
    return random.choice([0, 1])


def generate_promo_code():
    """Генерирует и возвращает промокод."""
    digits = ''.join(random.choices(string.digits, k=4))
    characters = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=8))
    return f'{digits}-{characters}'
