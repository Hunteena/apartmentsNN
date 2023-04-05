from django.contrib import admin

from flats.models import (
    Apartment,
    ApartmentImage,
    Comfort,
    DetailedCharacteristic,
    Location,
    MainPage,
    MainPageSliderImage
)


class DetailedInline(admin.TabularInline):
    model = DetailedCharacteristic
    extra = 0


class ComfortInline(admin.TabularInline):
    model = Comfort
    extra = 0


class LocationInline(admin.StackedInline):
    model = Location
    extra = 0


class ApartmentImageInline(admin.TabularInline):
    fields = ('group', 'photo', 'name', 'altName')
    model = ApartmentImage
    extra = 0


class MainPageSliderImageInline(admin.StackedInline):
    model = MainPageSliderImage
    extra = 0


class ApartmentAdmin(admin.ModelAdmin):
    inlines = [
        DetailedInline,
        ComfortInline,
        LocationInline,
        ApartmentImageInline
    ]

    fields = (
        'name',
        'title',
        'address',
        'description',
        'price',
        'capacity',
        'shortCharacteristic'
    )

    list_display = ('name', 'shortCharacteristic', 'price')


class MainPageAdmin(admin.ModelAdmin):
    inlines = [MainPageSliderImageInline]


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(MainPage, MainPageAdmin)
