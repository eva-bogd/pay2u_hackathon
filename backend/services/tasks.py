# tasks.py (Celery tasks file)

from datetime import datetime, timedelta

from api.utils import PAYMENT_DENIED, PAYMENT_SUCCESS, simulate_payment_status
from celery import shared_task

from .models import Transaction, UserTariff


@shared_task()
def make_payments():
    """Делает оплаты по тарифам с автопродлением."""
    now = datetime.now().date()
    tariffs_to_pay = UserTariff.objects.filter(
        auto_renewal=True,
        end_date__lte=now
    )
    denied_transactions = Transaction.objects.filter(
        payment_status=PAYMENT_DENIED
    )
    for user_tariff in tariffs_to_pay:
        # добавить логику отправки запроса в банк на оплату
        # сейчас делаем симуляцию ответа из банка со статусом оплаты
        # где 0 - отказано, 1 - оплачено
        payment_status = simulate_payment_status()
        # объект будет один, т.к. мы меняем данные
        # и создаем новые объекты по транзакциям
        # только если платеж прошел
        transaction = denied_transactions.filter(user_tariff=user_tariff)
        is_denied = transaction.exists()
        if not is_denied:
            Transaction.objects.create(
                user=user_tariff.user,
                user_tariff=user_tariff,
                date=now,
                amount=user_tariff.tariff.price,
                cashback=user_tariff.tariff.cashback,
                payment_status=payment_status,
            )
        if payment_status == PAYMENT_SUCCESS:
            end_date = now + timedelta(days=30 * user_tariff.tariff.period)
            user_tariff.end_date = end_date
            user_tariff.start_date = now
            user_tariff.save()
            if is_denied:
                transaction.date = now
                transaction.payment_status = payment_status
                transaction.save()
