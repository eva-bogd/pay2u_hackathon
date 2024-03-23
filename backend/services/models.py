from django.db import models
from users.models import User


class Subscription(models.Model):
    """
    Модель, представляющая подписку на сервис.
    """
    name = models.CharField(
        verbose_name='Service name',
        max_length=100,
        unique=True)
    logo = models.ImageField(
        verbose_name='Logo image',
        upload_to='services/images/')
    description = models.TextField(
        verbose_name='Description')
    usage_policy = models.TextField(
        verbose_name='Usage Policy')

    def __str__(self):
        return self.name


class Tariff(models.Model):
    """
    Модель, представляющая тарифные планы для подписки на сервис.
    """
    name = models.CharField(
        verbose_name='Tariff name',
        max_length=100,
        unique=True)
    subscription = models.ForeignKey(
        Subscription,
        verbose_name='Subscription',
        on_delete=models.CASCADE,
        related_name='tariffs')
    description = models.TextField(
        verbose_name='Description')
    duration = models.DurationField(
        verbose_name='Duration')
    price = models.DecimalField(
        verbose_name='Price',
        max_digits=10,
        decimal_places=2)
    test_period = models.DurationField(
        verbose_name='Test period',
        blank=True,
        null=True)
    test_price = models.DecimalField(
        verbose_name='Test price',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True)
    cashback = models.DecimalField(
        verbose_name='Сashback amount',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True)
    cashback_conditions = models.TextField(
        verbose_name='Cashback conditions')
    is_direct = models.BooleanField(
        verbose_name='Direct subscription',
        default=True)

    def __str__(self):
        return self.name


class UserTariff(models.Model):
    """
    Модель, представляющая тарифный план пользователя по подписке.
    """
    user = models.ForeignKey(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='user_tariffs')
    tariff = models.ForeignKey(
        Tariff,
        verbose_name='Tariff',
        on_delete=models.CASCADE,
        related_name='user_tariffs')
    start_date = models.DateField(
        verbose_name='Start date')
    end_date = models.DateField(
        verbose_name='End date',
        blank=True,
        null=True)
    is_active = models.BooleanField(
        verbose_name='Active subscription',
        default=True)
    auto_renewal = models.BooleanField(
        verbose_name='Auto renewal tariff',
        default=True)

    class Meta:
        unique_together = ['user', 'tariff']

    def __str__(self):
        f'{self.user}: {self.tariff.name}'


class Transaction(models.Model):
    """
    Модель, представляющая транзакции по оплате тарифа пользователя.
    """
    STATUS_CHOICES = [
        (0, 'Отказано'),
        (1, 'Зачислено'),
        (2, 'Ожидается')
    ]
    # Транзакция останется в базе при удалении тарифа пользователя?
    user_tariff = models.ForeignKey(
        UserTariff,
        verbose_name='User Tariff',
        on_delete=models.SET_NULL,
        null=True)
    date = models.DateField(
        verbose_name='Transaction date')
    amount = models.DecimalField(
        verbose_name='Transaction amount',
        max_digits=10,
        decimal_places=2)
    # Уточнить: какой тип данных будет храниться в статусе оплаты?
    payment_status = models.PositiveSmallIntegerField(
        verbose_name='Payment Status',
        choices=STATUS_CHOICES,
        default=2
    )

    def __str__(self):
        return f'{self.date}: {self.amount}'
