from api.validators import MODELS_RESTRICTIONS
from django.contrib.auth.models import AbstractUser
from django.db import models


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
        default='Иван',
    )
    last_name = models.CharField(
        max_length=MODELS_RESTRICTIONS['max_length'],
        blank=False,
        verbose_name='Фамилия',
        help_text='Введите фамилию пользователя',
        default='Иванов',
    )
    father_name = models.CharField(
        max_length=MODELS_RESTRICTIONS['max_length'],
        verbose_name='Отчество',
        help_text='Введите отчетство пользователя',
        default='Иванович',
    )
    phone_number = models.CharField(
        max_length=MODELS_RESTRICTIONS['middle_length'],
        blank=False,
        verbose_name='Номер телефона',
        help_text='Введите номер телефона в формате +7 (111) 111-11-11',
        default='+7 (111) 111-11-11',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
