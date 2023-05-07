import logging
from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.db.models import Max

from booking.emails import send_pre_booking_cancelled
from booking.models import Booking, Status, update_status_log

PREBOOKING_LIFETIME = 48

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = f'Меняет статус бронирования на cancelled, если бронирование ' \
           'находится в статусе inwork больше {PREBOOKING_LIFETIME} часов'

    def handle(self, *args, **options):
        # print(logger)
        # self.stdout.write(f"----- Checking bookings... -----")
        logger.debug("Checking bookings...")
        treshold = datetime.now() - timedelta(hours=PREBOOKING_LIFETIME)
        prebookings = Booking.objects.filter(
            status=Status.inwork,
            statuses__created_at__lt=treshold
        ).annotate(
            last_record=Max('statuses__created_at')
        )
        # print(prebookings)
        for booking in prebookings:
            logger.debug(f'Cancelling booking {booking}...')
            booking.status = Status.cancelled
            booking.save()
            logger.debug('Booking cancelled')
            update_status_log(booking=booking, status=Status.cancelled)
            send_pre_booking_cancelled(booking)
            logger.info(f"Автоматическая отмена бронирования '{booking}'")
