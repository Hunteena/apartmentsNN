from drf_spectacular.utils import extend_schema, inline_serializer, \
    extend_schema_serializer, OpenApiExample
from rest_framework import serializers, fields

from .models import Apartment, Comfort, DetailedCharacteristic, Image, Location


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        # fields = '__all__'
        exclude = ['id', 'apartment']


class DetailedCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailedCharacteristic
        # fields = '__all__'
        exclude = ['id', 'apartment']


class ComfortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comfort
        # fields = '__all__'
        exclude = ['id', 'apartment']


class LocationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['desc'] = [el.strip() for el in ret['desc'].split(',')]
        return ret

    class Meta:
        model = Location
        # fields = ['url', 'desc']
        exclude = ['id', 'apartment']


class ApartmentSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    detailedCharacteristic = DetailedCharacteristicSerializer(many=True)
    comfort = ComfortSerializer(many=True)
    location = LocationSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['shortCharacteristic'] = [
            el.strip() for el in ret['shortCharacteristic'].split(',')
        ]
        return ret

    class Meta:
        model = Apartment
        fields = '__all__'
