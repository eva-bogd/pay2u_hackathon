from django.db import models
from users.models import User


class Subscription(models.Model):
    """
    Модель, представляющая подписку на сервис.
    """
    name = models.CharField(
        verbose_name='Название сервиса',
        max_length=100,
        unique=True)
    logo = models.ImageField(
        verbose_name='Логотип',
        upload_to='services/images/',
        blank=True,
        null=True)
    description = models.TextField(
        verbose_name='Описание')
    partner_rules = models.TextField(
        verbose_name='Правила партнера')
    personal_data_policy = models.TextField(
        verbose_name='Политика обработки ПД')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.name


class Tariff(models.Model):
    """
    Модель, представляющая тарифные планы для подписки на сервис.
    """

    class PeriodChoices(models.IntegerChoices):
        ONE_MONTH = 1, '1 месяц'
        THREE_MONTHS = 3, '3 месяца'
        SIX_MONTHS = 6, '6 месяцев'
        TWELVE_MONTHS = 12, '12 месяцев'

    name = models.CharField(
        verbose_name='Название тарифа',
        max_length=100,
        unique=True)
    subscription = models.ForeignKey(
        Subscription,
        verbose_name='Подписка',
        on_delete=models.CASCADE,
        related_name='tariffs')
    description = models.TextField(
        verbose_name='Описание')
    # period = models.PositiveSmallIntegerField(
    #     verbose_name='Срок')
    period = models.PositiveSmallIntegerField(
        verbose_name='Срок',
        choices=PeriodChoices.choices)
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2)
    # test_period = models.PositiveSmallIntegerField(
    #     verbose_name='Пробный период',
    #     blank=True,
    #     null=True)
    test_period = models.PositiveSmallIntegerField(
        verbose_name='Пробный период',
        choices=PeriodChoices.choices,
        blank=True,
        null=True)
    test_price = models.DecimalField(
        verbose_name='Цена для пробного периода',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True)
    cashback = models.DecimalField(
        verbose_name='Кешбэк',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True)
    cashback_conditions = models.TextField(
        verbose_name='Условия начисления кешбэка')

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name


class UserTariff(models.Model):
    """
    Модель, представляющая тарифный план пользователя по подписке.
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='user_tariffs')
    tariff = models.ForeignKey(
        Tariff,
        verbose_name='Тариф',
        on_delete=models.CASCADE,
        related_name='user_tariffs')
    start_date = models.DateField(
        verbose_name='Дата начала')
    end_date = models.DateField(
        verbose_name='Дата окончания',
        blank=True,
        null=True)
    auto_renewal = models.BooleanField(
        verbose_name='Aвтопродление',
        default=True)
    is_direct = models.BooleanField(
        verbose_name='Прямая подписка',
        default=False)

    class Meta:
        verbose_name = 'Тариф пользователя'
        verbose_name_plural = 'Тарифы пользователя'
        unique_together = ['user', 'tariff']

    def __str__(self):
        return f'{self.user.email}: {self.tariff.name}'


class Transaction(models.Model):
    """
    Модель, представляющая транзакции по оплате тарифа пользователя.
    """
    STATUS_CHOICES = [
        (0, 'Отказано'),
        (1, 'Зачислено')
    ]
    # Транзакция останется в базе при удалении тарифа пользователя?
    user = models.ForeignKey(
        User,
        verbose_name="Оплата",
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions")
    user_tariff = models.ForeignKey(
        UserTariff,
        verbose_name='Тариф пользователя',
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions')
    date = models.DateField(
        verbose_name='Дата оплаты',
        blank=True,
        null=True)
    amount = models.DecimalField(
        verbose_name='Сумма',
        max_digits=10,
        decimal_places=2)
    cashback = models.DecimalField(
        verbose_name='Кешбэк',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True)
    # Уточнить: какой тип данных будет храниться в статусе оплаты?
    payment_status = models.PositiveSmallIntegerField(
        verbose_name='Статус оплаты',
        choices=STATUS_CHOICES,
        default=0)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Оплата'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.date}: {self.amount}'
