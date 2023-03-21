from django.shortcuts import render
from drf_spectacular.utils import extend_schema, inline_serializer, \
    OpenApiExample
from rest_framework import fields
from rest_framework.viewsets import ReadOnlyModelViewSet

from flats.models import Apartment
from flats.serializers import ApartmentSerializer
from backend.schema import BOOKING_SCHEMA_EXAMPLE


@extend_schema(
    examples=[OpenApiExample('response', value=BOOKING_SCHEMA_EXAMPLE)]
)
class ApartmentViewSet(ReadOnlyModelViewSet):
    """
    Класс для просмотра информации о квартирах
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
