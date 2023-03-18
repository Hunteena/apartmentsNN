from django.core.exceptions import ValidationError
from django.db import models

from flats.models import Apartment
from users.models import User


class Status(models.TextChoices):
    inwork = 'inwork', 'В работе'
    confirmed = 'confirmed', 'Подтверждено'
    cancelled = 'cancelled', 'Отменено'


class Booking(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        verbose_name='Апартаменты',
        help_text='Выберите апартаменты для бронирования'
    )
    dateFrom = models.DateField(
        verbose_name='Дата начала',
        help_text='Выберите дату начала бронирования'
    )
    dateTo = models.DateField(
        verbose_name='Дата окончания',
        help_text='Выберите дату окончания бронирования'
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Имя',
        help_text='Введите имя гостя'
    )
    phone = models.CharField(
        max_length=32,
        verbose_name='Номер телефона',
        help_text='Введите номер телефона гостя'
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text='Введите электронную почту гостя'
    )
    status = models.CharField(
        verbose_name='Статус бронирования',
        help_text='Выберите статус бронирования',
        max_length=16,
        choices=Status.choices,
        default=Status.inwork
    )
    # admin = models.ForeignKey(
    #     User,
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET('Администратор был удалён'),
    #     verbose_name='Администратор',
    #     help_text='Администратор, принявший решение о принятии или отклонении брони',
    # )

    def clean(self):
        if self.dateFrom > self.dateTo:
            raise ValidationError(
                {'dateTo': 'Дата окончания не может быть раньше даты начала'}
            )

    def __str__(self):
        return (f"{self.apartment}: {self.dateFrom} - {self.dateTo}. "
                f"Гость: {self.name}")

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Список бронирований'

