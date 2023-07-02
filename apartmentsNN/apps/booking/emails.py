import logging

from django.conf import settings
from django.core import mail
from django.urls import reverse

from apps.booking.models import EmailText, EmailType
from apps.flats.models import Apartment
from apps.users.models import User

logger = logging.getLogger(__name__)


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


def get_email_template(booking, template_type: EmailType) -> tuple:
    apartment = Apartment.objects.get(id=booking.apartment.id)
    booking_info = (
        f"Информация о бронировании:\n"
        f"апартаменты {booking.apartment},\n"
        f"адрес {apartment.address},\n"
        f"даты {booking.dateFrom} - {booking.dateTo}.\n\n"
    )

    try:
        email_text = EmailText.objects.get(type=template_type)
    except EmailText.DoesNotExist:
        logger.warning(f'No email template for {template_type}')
        return template_type, booking_info

    subject = email_text.subject
    body = (
        f"{email_text.before_name} "
        f"{booking.name}.\n\n"
        f"{email_text.after_name}\n\n"
        f"{booking_info}"
        f"{email_text.after_booking_info}"
    )
    return subject, body


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
    subject, body = get_email_template(booking, EmailType.prebooking)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [booking.email]
    email = mail.EmailMessage(subject, body, from_email, to)
    email.send()


def send_pre_booking_cancelled(booking):
    logger.debug('Sending email...')
    subject, body = get_email_template(booking, EmailType.cancel)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [booking.email]
    email = mail.EmailMessage(subject, body, from_email, to)
    email.send()
    logger.debug('Email sent')
