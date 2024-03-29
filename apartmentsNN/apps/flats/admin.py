from django.contrib import admin

from apps.flats.models import (
    Apartment,
    ApartmentImage,
    Comfort,
    Location,
    MainPage,
    MainPageSliderImage
)


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
        ComfortInline,
        LocationInline,
        ApartmentImageInline
    ]
    fieldsets = (
        (None, {'fields': (
            ('name', 'owner'),
            'title',
            'address',
            'description',
            'price',
            'capacity',
            'shortCharacteristic'
        )}),
        ('Характеристики', {'fields': (
            'rooms', 'store', 'area', 'year'
        )})
    )

    list_display = ('name', 'shortCharacteristic', 'price', 'owner')


class MainPageAdmin(admin.ModelAdmin):
    inlines = [MainPageSliderImageInline]


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(MainPage, MainPageAdmin)
