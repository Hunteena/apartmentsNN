from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from backend.schema import BOOKING_SCHEMA_EXAMPLE
from apps.booking.models import Booking, get_reserved_dates
from apps.booking.serializers import BookingSerializer, ReservedDatesSerializer


@extend_schema(
    examples=[OpenApiExample('request', value=BOOKING_SCHEMA_EXAMPLE, request_only=True)]
)
class BookingCreateAPIView(generics.CreateAPIView):
    """
    Класс для создания бронирования
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class ReservedDatesAPIView(APIView):
    """
    Класс для получения забронированных дат
    """
    serializer_class = ReservedDatesSerializer(many=True)

    def get(self, request, apartment_id=None):
        """
        Возвращает список забронированных дат
        """
        if apartment_id:
            dates = get_reserved_dates(apartment_id).get(apartment_id)
            reserved_dates = [{
                'id_apartment': apartment_id,
                'dates': dates
            }]
        else:
            reserved_dates = [
                {'id_apartment': ap_id, 'dates': dates}
                for ap_id, dates in get_reserved_dates().items()
            ]
        return Response(reserved_dates)
