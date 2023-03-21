from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from booking.models import Booking, check_period, get_reserved_dates, period


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

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status']


class ReservedDatesSerializer(serializers.Serializer):
    id_apartment = serializers.IntegerField()
    dates = serializers.ListField(default=[])
