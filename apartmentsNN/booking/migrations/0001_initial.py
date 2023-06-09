# Generated by Django 4.1.7 on 2023-03-18 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flats', '0004_alter_apartment_options_alter_comfort_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateFrom', models.DateField(help_text='Выберите дату начала бронирования', verbose_name='Дата начала')),
                ('dateTo', models.DateField(help_text='Выберите дату окончания бронирования', verbose_name='Дата окончания')),
                ('name', models.CharField(help_text='Введите имя гостя', max_length=256, verbose_name='Имя')),
                ('phone', models.CharField(help_text='Введите номер телефона гостя', max_length=32, verbose_name='Номер телефона')),
                ('email', models.EmailField(help_text='Введите электронную почту гостя', max_length=254, verbose_name='Электронная почта')),
                ('status', models.CharField(choices=[('inwork', 'В работе'), ('confirmed', 'Подтверждено'), ('cancelled', 'Отменено')], default='inwork', help_text='Выберите статус бронирования', max_length=16, verbose_name='Статус бронирования')),
                ('apartment', models.ForeignKey(help_text='Выберите апартаменты для бронирования', on_delete=django.db.models.deletion.CASCADE, to='flats.apartment', verbose_name='Апартаменты')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Список бронирований',
            },
        ),
    ]
