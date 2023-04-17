from django.conf import settings
from django.core import mail
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from booking.models import Booking, check_period, get_reserved_dates, period
from users.models import User


def get_staff_emails(request):
    staff_emails = [
        el[0]
        for el in User.objects.filter(is_staff=True).values_list('email')
        if el[0]
    ]
    # print(staff_emails)
    if not any(staff_emails):
        subject = 'Невозможно уведомить о новой заявке на сайте Квартиры в Нижнем Новгороде'
        message = (
            'Нет персонала с электронной почтой! '
            'Поэтому нет возможности уведомить их о новой заявке на бронирование!'
        )
        if request:
            users_admin_absolute_url = request.build_absolute_uri(
                reverse('admin:users_user_changelist')
            )
            message += f"\n{users_admin_absolute_url}"
        # print(message)
        mail.mail_admins(subject, message)
    return staff_emails


def notify_staff(booking, request):
    subject = f"Новое бронирование {booking}"
    body = (
        f"Добрый день!\n\nНовая заявка на бронирование:\n"
        f"апартаменты {booking.apartment},\n"
        f"даты {booking.dateFrom} - {booking.dateTo},\n"
        f"гость {booking.name},\n"
        f"телефон гостя {booking.phone},\n"
        f"электронная почта гостя {booking.email}.\n"
    )
    if request:
        booking_admin_absolute_url = request.build_absolute_uri(
            reverse('admin:booking_booking_change', args=(booking.id,))
        )
        body += f"\nДля подтверждения заявки {booking_admin_absolute_url}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = get_staff_emails(request)
    email = mail.EmailMessage(subject, body, from_email, to)
    email.send()


def send_pre_booking(booking):
    subject = 'Заявка на бронирование'
    body = (
        f"Добрый день, {booking.name}!\n\n"
        f"Вы оставили заявку на бронирование на сайте Квартиры в Нижнем Новгороде. "
        f"Менеджер свяжется с Вами в ближайшее время.\n\n"
        f"Информация о бронировании:\n"
        f"апартаменты {booking.apartment},\n"
        f"даты {booking.dateFrom} - {booking.dateTo}.\n"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [booking.email]
    email = mail.EmailMessage(subject, body, from_email, to)
    email.send()


class BookingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['dateFrom'] >= attrs['dateTo']:
            raise ValidationError('Дата окончания бронирования не может быть '
                                  'раньше даты начала или совпадать с ней')
        forbidden = check_period(
            period(attrs['dateFrom'], attrs['dateTo']),
            apartment_id=attrs['apartment'].id
        )
        if forbidden:
            raise ValidationError(
                f"Даты уже забронированы: {', '.join(forbidden)}"
            )
        return attrs

    def create(self, validated_data):
        booking = super().create(validated_data)
        if booking:
            notify_staff(booking, self.context.get('request', None))
            send_pre_booking(booking)
        return booking

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status']


class ReservedDatesSerializer(serializers.Serializer):
    id_apartment = serializers.IntegerField()
    dates = serializers.ListField(default=[])
