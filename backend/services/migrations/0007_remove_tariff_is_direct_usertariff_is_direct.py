# Generated by Django 4.2 on 2024-03-25 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_tariff_is_direct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariff',
            name='is_direct',
        ),
        migrations.AddField(
            model_name='usertariff',
            name='is_direct',
            field=models.BooleanField(default=True, verbose_name='Прямая подписка'),
        ),
    ]
