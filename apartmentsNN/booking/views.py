import datetime

from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, inline_serializer, \
    OpenApiExample

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from booking.models import Booking
from booking.serializers import BookingSerializer, ReservedDatesSerializer
from booking.utils import get_reserved_dates


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
    # queryset = Booking.objects.filter(
    #     Q(status='inwork') | Q(status='confirmed')
    # ).only('apartment', 'dateFrom', 'dateTo')
    serializer_class = ReservedDatesSerializer(many=True)

    # @extend_schema(
    #     responses=ReservedDatesSerializer()
    #     # examples=[OpenApiExample(
    #     #     name='reserved dates',
    #     #     response_only=True,
    #     #     value={"1": ["2023-03-18","2023-03-19"]}
    #     # )]
    # )
    def get(self, request):
        """
        Возвращает список забронированных дат для каждой квартиры
        """
        queryset = Booking.objects.filter(
            Q(status='inwork') | Q(status='confirmed')
        ).only('apartment', 'dateFrom', 'dateTo')
        reserved_dates = [
            {'id_apartment': apartment_id, 'dates': dates}
            for apartment_id, dates in get_reserved_dates(queryset).items()
        ]
        return Response(reserved_dates)
