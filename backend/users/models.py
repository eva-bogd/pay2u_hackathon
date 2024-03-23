from api.validators import MODELS_RESTRICTIONS
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """ Кастомный User """

    email = models.EmailField(
        max_length=MODELS_RESTRICTIONS['max_length'],
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты',
    )

    first_name = models.CharField(
        max_length=MODELS_RESTRICTIONS['max_length'],
        blank=False,
        verbose_name='Имя',
        help_text='Введите имя пользователя',
    )

    last_name = models.CharField(
        max_length=MODELS_RESTRICTIONS['max_length'],
        blank=False,
        verbose_name='Фамилия',
        help_text='Введите фамилию пользователя',
    )

    father_name = models.CharField(
        max_length=MODELS_RESTRICTIONS['max_length'],
        verbose_name='Отчество',
        help_text='Введите отчетство пользователя',
    )

    phone_number = models.CharField(
        blank=False,
        verbose_name='Номер телефона',
        help_text='Введите номер телефона в формате +7 (111) 111-11-11',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.last_name}'
