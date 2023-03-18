import datetime

from django.db.models import Q
from django.shortcuts import render

from booking.models import Booking
from booking.serializers import BookingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics


class BookingCreateView(generics.CreateAPIView):
    """
    Класс для создания бронирования
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class ReservedDatesView(APIView):
    """
    Класс для получения забронированных дат
    """
    def get(self, request):
        """
        Возвращает список забронированных дат для каждой квартиры
        """
        queryset = Booking.objects.filter(
            Q(status='inwork') | Q(status='confirmed')
        )
        reserved = {}
        for booking in queryset:
            d = booking.dateFrom
            dates = [d]
            while d < booking.dateTo:
                d += datetime.timedelta(days=1)
                dates.append(d)
            apartment_id = reserved.get(booking.apartment.id)
            if apartment_id:
                reserved[booking.apartment.id] += dates
            else:
                reserved[booking.apartment.id] = dates
        return Response(reserved)


