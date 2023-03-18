from django.contrib import admin

from .models import Apartment, Comfort, DetailedCharacteristic, Image, Location


class DetailedInline(admin.TabularInline):
    model = DetailedCharacteristic
    extra = 0


class ComfortInline(admin.TabularInline):
    model = Comfort
    extra = 0


class LocationInline(admin.StackedInline):
    model = Location
    extra = 0


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class ApartmentAdmin(admin.ModelAdmin):
    inlines = [DetailedInline, ComfortInline, LocationInline, ImageInline]

    fields = (
        'name',
        'title',
        'address',
        'description',
        'price',
        'capacity',
        'shortCharacteristic')

    list_display = ('name', 'shortCharacteristic', 'price')


admin.site.register(Apartment, ApartmentAdmin)
