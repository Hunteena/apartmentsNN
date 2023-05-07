import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from booking.emails import notify_staff, send_pre_booking
from booking.models import Booking, check_period, period

logger = logging.getLogger(__name__)


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
            logger.info(f"Заявка на бронирование на сайте '{booking}'")
        return booking

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status']


class ReservedDatesSerializer(serializers.Serializer):
    id_apartment = serializers.IntegerField()
    dates = serializers.ListField(default=[])
