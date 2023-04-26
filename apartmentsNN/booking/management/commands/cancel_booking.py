import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.core import mail
from django.core.management import BaseCommand
from django.db.models import Max

from booking.models import Booking, Status, update_status_log

PREBOOKING_LIFETIME = 48

logger = logging.getLogger(__name__)


def send_pre_booking_cancelled(booking):
    subject = 'Отмена заявки на бронирование'
    body = (
        f"Добрый день, {booking.name}!\n\n"
        f"Вы оставляли заявку на бронирование на сайте Квартиры в Нижнем Новгороде.\n"
        f"Информация о бронировании:\n"
        f"апартаменты {booking.apartment},\n"
        f"даты {booking.dateFrom} - {booking.dateTo}.\n\n"
        f"К сожалению, менеджеру не удалось связаться с Вами в течение "
        f"{PREBOOKING_LIFETIME} часов, поэтому Ваша заявка была отменена.\n\n"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [booking.email]
    email = mail.EmailMessage(subject, body, from_email, to)
    email.send()


class Command(BaseCommand):
    help = 'Меняет статус бронирования на cancelled, если бронирование ' \
           'находится в статусе inwork больше 48 часов'

    def handle(self, *args, **options):
        treshold = datetime.now() - timedelta(hours=PREBOOKING_LIFETIME)
        prebookings = Booking.objects.filter(
            status=Status.inwork,
            statuses__created_at__lt=treshold
        ).annotate(
            last_record=Max('statuses__created_at')
        )
        # print(prebookings)
        for booking in prebookings:
            # self.stdout.write(booking.id)
            # print(booking)
            booking.status = Status.cancelled
            booking.save()
            update_status_log(booking=booking, status=Status.cancelled)
            send_pre_booking_cancelled(booking)
            logger.info(f"Автоматическая отмена бронирования '{booking}'")
