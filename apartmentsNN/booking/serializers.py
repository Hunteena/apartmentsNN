import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from booking.models import Booking

from booking.utils import get_reserved_dates


class BookingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['dateFrom'] >= attrs['dateTo']:
            raise ValidationError('Дата окончания бронирования не может быть '
                                  'раньше даты начала или совпадать с ней')
        return attrs

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status']


# class ReservedDatesListSerializer(serializers.ListSerializer):
#     def to_representation(self, instance):
#         print(instance)
#         # ret = super().to_representation(instance)
#         ret = get_reserved_dates(instance)
#         print(ret)
#         return ret
#
class ReservedDatesSerializer(serializers.Serializer):
    id_apartment = serializers.IntegerField()
    dates = serializers.ListField(default=[])

    # def to_representation(self, instance):


    # class Meta:
    #     list_serializer_class = ReservedDatesListSerializer
