import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from booking.emails import notify_staff, send_pre_booking
from booking.models import Booking, check_period, period, Status

logger = logging.getLogger(__name__)


class BookingSerializer(serializers.ModelSerializer):
    crossDates = serializers.BooleanField(write_only=True, required=False)
    guests = serializers.DictField(write_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        guests = data.pop('guests')
        data['adults'] = guests['adult']
        data['children'] = guests.get('children', 0)

        if data.get('crossDates') is not None:
            cross_dates = data.pop('crossDates')
            data['status'] = Status.pending if cross_dates else Status.inwork
        return data

    def validate(self, attrs):
        if attrs['dateFrom'] >= attrs['dateTo']:
            raise ValidationError('Дата окончания бронирования не может быть '
                                  'раньше даты начала или совпадать с ней')
        if not attrs['status'] == Status.pending:
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
            logger.info(f"Заявка на бронирование на сайте '{booking}'")
        return booking

    class Meta:
        model = Booking
        fields = (
            'id', 'apartment',
            'dateFrom', 'dateTo',
            'name', 'phone', 'email',
            'status',
            'adults', 'children', 'guests',
            'crossDates',
        )
        read_only_fields = ['status']


class ReservedDatesSerializer(serializers.Serializer):
    id_apartment = serializers.IntegerField()
    dates = serializers.ListField(default=[])
