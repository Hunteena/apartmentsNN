from rest_framework import serializers

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
    class Meta:
        model = Location
        # fields = '__all__'
        exclude = ['id', 'apartment']


class ApartmentSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    detailed = DetailedCharacteristicSerializer(many=True)
    comfort = ComfortSerializer(many=True)
    location = LocationSerializer()

    class Meta:
        model = Apartment
        fields = '__all__'
