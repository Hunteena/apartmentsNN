import datetime

from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, inline_serializer, \
    OpenApiExample

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from booking.models import Booking, get_reserved_dates
from booking.serializers import BookingSerializer, ReservedDatesSerializer


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
            reserved_dates = [{
                'id_apartment': apartment_id,
                'dates': get_reserved_dates(apartment_id).get(apartment_id)
            }]
        else:
            reserved_dates = [
                {'id_apartment': ap_id, 'dates': dates}
                for ap_id, dates in get_reserved_dates().items()
            ]
        return Response(reserved_dates)
