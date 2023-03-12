from django.contrib import admin

from .models import Apartment, Comfort, DetailedCharacteristic, Image, Location


class DetailedInline(admin.StackedInline):
    model = DetailedCharacteristic
    extra = 0


class ComfortInline(admin.StackedInline):
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

    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'title', 'description', 'capacity', 'price')
    #     }),
    #     ('Расположение', {
    #         'fields': ('address', LocationInline),
    #     }),
    #     ('Характеристики', {
    #         'fields': ('shortCharacteristic', 'detailed', 'comfort'),
    #     }),
    # )
    fields = (
        'name',
        'title',
        'address',
        'description',
        'price',
        'capacity',
        'shortCharacteristic')


admin.site.register(Apartment, ApartmentAdmin)
