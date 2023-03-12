from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Apartment
from .serializers import ApartmentSerializer


class ApartmentViewSet(ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    http_method_names = ['get']