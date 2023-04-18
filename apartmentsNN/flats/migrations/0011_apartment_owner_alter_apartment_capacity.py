# Generated by Django 4.1.7 on 2023-04-18 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flats', '0010_alter_comfort_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Выберите владельца', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apartments', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='capacity',
            field=models.PositiveSmallIntegerField(help_text='Введите максимальную вместимость', verbose_name='Максимальная вместимость'),
        ),
    ]
