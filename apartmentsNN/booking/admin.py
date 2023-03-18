from django.contrib import admin

from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('apartment', 'status')}),
        ('Даты', {'fields': (('date_from', 'date_to'),)}),
        ('Информация о госте', {'fields': ('name', 'phone', 'email',)})
    )
    # readonly_fields = ('admin',)
    list_filter = ('apartment', 'status', 'date_from', 'date_to')
    list_display = ('dates', 'apartment', 'status')

    @admin.display(description='Даты')
    def dates(self, obj):
        return f"{obj.date_from} - {obj.date_to}"


admin.site.register(Booking, BookingAdmin)
