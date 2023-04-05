from itertools import groupby

from rest_framework import serializers

from flats.models import (
    Apartment,
    ApartmentImage,
    Comfort,
    DetailedCharacteristic,
    Image,
    Location,
    MainPage
)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo', 'name', 'altName']
        # exclude = ['id', 'apartment']


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImage
        fields = ['photo', 'name', 'altName', 'group']


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
    images = ApartmentImageSerializer(many=True)
    detailedCharacteristic = DetailedCharacteristicSerializer(many=True)
    comfort = ComfortSerializer(many=True)
    location = LocationSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['shortCharacteristic'] = [
            el.strip() for el in ret['shortCharacteristic'].split(',')
        ]
        images = ret.get('images')
        if images:
            ret['images'] = {
                k: list(g)
                for k, g in groupby(images, key=lambda x: x['group'])
            }

        return ret

    class Meta:
        model = Apartment
        fields = '__all__'


class MainPageSerializer(serializers.ModelSerializer):
    slider_images = ImageSerializer(many=True)

    class Meta:
        model = MainPage
        fields = '__all__'
