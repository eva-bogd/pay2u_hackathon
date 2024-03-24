# Generated by Django 4.2 on 2024-03-23 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertariff',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tariffs', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user_tariff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.usertariff', verbose_name='User Tariff'),
        ),
        migrations.AddField(
            model_name='tariff',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tariffs', to='services.subscription', verbose_name='Subscription'),
        ),
        migrations.AlterUniqueTogether(
            name='usertariff',
            unique_together={('user', 'tariff')},
        ),
    ]
