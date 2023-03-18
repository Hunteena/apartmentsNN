from django.shortcuts import render
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import fields
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Apartment
from .serializers import ApartmentSerializer


class ApartmentViewSet(ReadOnlyModelViewSet):
    """
    Класс для просмотра информации о квартирах
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
