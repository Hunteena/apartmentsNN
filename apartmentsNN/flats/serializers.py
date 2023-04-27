from itertools import groupby

from rest_framework import serializers

from flats.models import (
    Apartment,
    ApartmentImage,
    Comfort,
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


class ComfortSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = {
            "type": instance.option,
            "description": instance.ComfortOptions(instance.option).label
        }
        return ret

    class Meta:
        model = Comfort
        # fields = '__all__'
        exclude = ['id', 'apartment']


class LocationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['desc'] = [el.strip() for el in ret['desc'].split(',')]
        ret['geoposition'] = [ret.pop('latitude'), ret.pop('longitude')]
        return ret

    class Meta:
        model = Location
        # fields = ['url', 'desc']
        exclude = ['id', 'apartment']


class ApartmentSerializer(serializers.ModelSerializer):
    images = ApartmentImageSerializer(many=True)
    comfort = ComfortSerializer(many=True)
    location = LocationSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['shortCharacteristic'] = [
            el.strip() for el in ret['shortCharacteristic'].split(',')
        ]
        images = ret.get('images')
        if images:
            groups = {
                k: list(g)
                for k, g in groupby(images, key=lambda x: x['group'])
            }
            ret['images'] = [
                groups[k] for k in sorted(groups.keys())
            ]

        detailed_fields = {
            'rooms': 'Комнат',
            'store': 'Этаж',
            'area': 'Общая площадь',
            'year': 'Год постройки'
        }
        ret['detailedCharacteristic'] = []
        for field, name in detailed_fields.items():
            ret['detailedCharacteristic'].append(
                {"name": name, "data": ret[field]}
            )
            ret.pop(field)
        return ret

    class Meta:
        model = Apartment
        fields = '__all__'


class MainPageSerializer(serializers.ModelSerializer):
    slider_images = ImageSerializer(many=True)

    class Meta:
        model = MainPage
        fields = '__all__'
