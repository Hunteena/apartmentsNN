from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet

from backend.schema import APARTMENT_SCHEMA_EXAMPLE
from flats.models import Apartment, MainPage
from flats.serializers import ApartmentSerializer, MainPageSerializer


# TODO избавиться от сложного примера ответа
@extend_schema(
    examples=[OpenApiExample('response', value=APARTMENT_SCHEMA_EXAMPLE)]
)
class ApartmentViewSet(ReadOnlyModelViewSet):
    """
    Класс для просмотра информации о квартирах
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class MainPageViewSet(generics.ListAPIView):
    """
    Класс для просмотра информации на главной странице
    """
    queryset = MainPage.objects.all()
    serializer_class = MainPageSerializer
