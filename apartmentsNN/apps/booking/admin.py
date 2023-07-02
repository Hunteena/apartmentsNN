from django.contrib import admin
from django.utils.html import format_html

from apps.booking.models import Booking, update_status_log, StatusLog, EmailText, \
    Status


class StatusLogInline(admin.TabularInline):
    model = StatusLog
    extra = 0
    fields = ('status', 'created_at', 'manager')
    readonly_fields = ('status', 'created_at', 'manager')
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


class StatusListFilter(admin.SimpleListFilter):
    title = 'Статус бронирования'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        lookups_tuple = (
            ('Active', 'Кроме отмененных'),
         )
        for status in Status.choices:
            lookups_tuple += (status, )
        # print(lookups_tuple)
        return lookups_tuple

    def queryset(self, request, queryset):
        match self.value():
            case None:
                return queryset.all()
            case 'Active':
                return queryset.exclude(status=Status.cancelled)
            case status:
                return queryset.filter(status=status)


class BookingAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = (
        (None, {'fields': ('apartment', 'status')}),
        ('Даты', {'fields': (('dateFrom', 'dateTo'),)}),
        ('Информация о госте', {'fields': ('name', 'phone', 'email',)}),
        (None, {'fields': ('adults', 'children')})
    )
    # readonly_fields = ('dateFrom', 'dateTo')
    list_filter = ('apartment', StatusListFilter, 'dateFrom', 'dateTo')
    list_display = ('dates', 'apartment', 'status', 'name', 'phone', 'guests')
    inlines = [StatusLogInline]
    ordering = ['-dateFrom']

    @admin.display(description='Даты')
    def dates(self, obj):
        return f"{obj.dateFrom} - {obj.dateTo}"

    @admin.display(description='Гости')
    def guests(self, obj):
        return f"Взрослых: {obj.adults}, детей: {obj.children}"

    def save_model(self, request, obj, form, change):
        previous_data = Booking.objects.get(pk=obj.pk)
        if previous_data and previous_data.status != obj.status:
            update_status_log(obj, obj.status, request.user)
        super().save_model(request, obj, form, change)


class EmailTextAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = (
        (None, {'fields': (
            ('type',),
            'subject', 'before_name', 'after_name', 'after_booking_info'
        )}),
    )
    list_display = ('type', 'subject', 'text')

    @admin.display(description='Текст шаблона')
    def text(self, obj):
        return format_html(
            f"<p>{obj.before_name}, <имя гостя>.</p>"
            f"<p>{obj.after_name}</p>"
            f"<p>Информация о бронировании:</p>"
            f"<p>апартаменты <название апартаментов>,</p>"
            f"<p>адрес <адрес апартаментов>,</p>"
            f"<p>даты <дата начала бронирования> - <дата окончания бронирования>.</p>"
            f"<p>{obj.after_booking_info}</p>"
        )


admin.site.register(Booking, BookingAdmin)
admin.site.register(EmailText, EmailTextAdmin)
