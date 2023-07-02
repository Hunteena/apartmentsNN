import logging
from datetime import timedelta

from django.core.management import BaseCommand
from django.db.models import Max
from django.utils import timezone

from apps.booking.emails import send_pre_booking_cancelled
from apps.booking.models import Booking, Status, update_status_log

PREBOOKING_LIFETIME = 48

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        f'Меняет статус бронирования на cancelled, если бронирование '
        'находится в статусе inwork или pending больше {PREBOOKING_LIFETIME} '
        'часов'
    )

    def handle(self, *args, **options):
        # print(logger)
        # self.stdout.write(f"----- Checking bookings... -----")
        logger.debug("Checking bookings...")
        treshold = timezone.now() - timedelta(hours=PREBOOKING_LIFETIME)
        expired_prebookings = Booking.objects.annotate(
            last_record=Max('statuses__created_at')
        ).filter(
            status__in=[Status.inwork, Status.pending],
            last_record__lt=treshold
        )
        # print(prebookings.values())
        # print(f"{treshold=}")
        for booking in expired_prebookings:
            logger.debug(f'Cancelling booking {booking}...')
            booking.status = Status.cancelled
            booking.save()
            logger.debug('Booking cancelled')
            update_status_log(booking=booking, status=Status.cancelled)
            send_pre_booking_cancelled(booking)
            logger.info(f"Автоматическая отмена бронирования '{booking}'")
