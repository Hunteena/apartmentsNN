# Generated by Django 4.1.7 on 2023-03-31 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0002_booking_datefrom_lte_dateto'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('inwork', 'В работе'), ('confirmed', 'Подтверждено'), ('cancelled', 'Отменено')], max_length=16, verbose_name='Статус бронирования')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Когда статус был изменен')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='booking.booking')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='statuses', to=settings.AUTH_USER_MODEL, verbose_name='Кто изменил статус')),
            ],
            options={
                'verbose_name': 'Изменение статуса',
                'verbose_name_plural': 'История статусов бронирования',
            },
        ),
    ]