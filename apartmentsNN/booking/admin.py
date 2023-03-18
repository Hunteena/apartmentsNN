from django.contrib import admin

from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('apartment', 'status')}),
        ('Даты', {'fields': (('dateFrom', 'dateTo'),)}),
        ('Информация о госте', {'fields': ('name', 'phone', 'email',)})
    )
    # readonly_fields = ('admin',)
    list_filter = ('apartment', 'status', 'dateFrom', 'dateTo')
    list_display = ('dates', 'apartment', 'status')

    @admin.display(description='Даты')
    def dates(self, obj):
        return f"{obj.dateFrom} - {obj.dateTo}"


admin.site.register(Booking, BookingAdmin)
