from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.db.models import Max

from booking.models import Booking, Status, update_status_log

PREBOOKING_LIFETIME = 48


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
            # self.stdout.write(p.id)
            # print(booking.last_record)
            booking.status = Status.cancelled
            booking.save()
            update_status_log(booking=booking, status=Status.cancelled)
