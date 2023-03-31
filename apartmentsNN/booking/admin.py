from django.contrib import admin

from booking.models import Booking, update_status_log, StatusLog


class StatusLogInline(admin.TabularInline):
    model = StatusLog
    extra = 0
    fields = ('status', 'created_at', 'manager')
    readonly_fields = ('status', 'created_at', 'manager')
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


class BookingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('apartment', 'status')}),
        ('Даты', {'fields': (('dateFrom', 'dateTo'),)}),
        ('Информация о госте', {'fields': ('name', 'phone', 'email',)})
    )
    # readonly_fields = ('dateFrom', 'dateTo')
    list_filter = ('apartment', 'status', 'dateFrom', 'dateTo')
    list_display = ('dates', 'apartment', 'status', 'name', 'phone')
    inlines = [StatusLogInline]

    @admin.display(description='Даты')
    def dates(self, obj):
        return f"{obj.dateFrom} - {obj.dateTo}"

    def save_model(self, request, obj, form, change):
        previous_data = Booking.objects.get(pk=obj.pk)
        if previous_data and previous_data.status != obj.status:
            update_status_log(obj, obj.status, request.user)
        super().save_model(request, obj, form, change)


admin.site.register(Booking, BookingAdmin)
