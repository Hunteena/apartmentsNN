import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from flats.models import Apartment


def get_reserved_dates(apartment_id: int = None) -> dict:
    """
    Возвращает словарь, где id апартаментов сопоставлен список забронированных дат
    """
    query = Q(status='inwork') | Q(status='confirmed')
    if apartment_id:
        query = query & Q(apartment=apartment_id)
    queryset = Booking.objects.filter(query).only(
        'apartment', 'dateFrom', 'dateTo'
    )
    reserved = {}
    for booking in queryset:
        d = booking.dateFrom
        dates = [d]
        while d < booking.dateTo:
            d += datetime.timedelta(days=1)
            dates.append(d)
        # print(dates)
        if reserved.get(booking.apartment.id):
            reserved[booking.apartment.id] += dates
        else:
            reserved[booking.apartment.id] = dates
        # print(reserved[booking.apartment.id])
    for apartment in reserved:
        reserved[apartment].sort()

    return reserved


def check_period(period_to_check: list[datetime], apartment_id: int,
                 exclude: list[datetime] = None) -> list[datetime]:
    """
    Возвращает для апартаментов с id=apartment_id список дат из period_to_check
    (за исключением дат из exclude), которые недоступны для бронирования
    """
    result = []
    reserved = get_reserved_dates(apartment_id)
    if exclude:
        period_to_check = set(period_to_check).difference(exclude)
    for d in period_to_check:
        if d in reserved[apartment_id]:
            result.append(d.isoformat())
    # print(reserved)
    # print(set(period_to_check).difference(exclude))
    # print(result)
    result.sort()
    return result


def period(start: datetime, end: datetime) -> list[datetime]:
    """
    Возвращает список дат от start до end включительно
    """
    result = []
    d = start
    while d <= end:
        result.append(d)
        d += datetime.timedelta(days=1)
    # print(result)
    return result


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

    def clean(self):
        if self.pk:
            previous_data = self.__class__.objects.get(pk=self.pk)
            if previous_data.status in (Status.inwork, Status.confirmed):
                dates_to_exclude = period(previous_data.dateFrom, previous_data.dateTo)
            else:
                dates_to_exclude = None
            forbidden = check_period(
                period(self.dateFrom, self.dateTo),
                apartment_id=self.apartment.id,
                exclude=dates_to_exclude
            )
            # print(forbidden)
            if forbidden:
                raise ValidationError(f"Даты уже забронированы: {', '.join(forbidden)}")

    def __str__(self):
        return (f"{self.apartment}: {self.dateFrom} - {self.dateTo}. "
                f"Гость: {self.name}")

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Список бронирований'
        constraints = [models.CheckConstraint(
            check=Q(dateFrom__lt=models.F('dateTo')),
            name='dateFrom_lte_dateTo',
            violation_error_message='Дата окончания бронирования не может быть'
                                    ' раньше даты начала или совпадать с ней'
        )]
