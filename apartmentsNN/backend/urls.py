from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, \
    SpectacularRedocView
from rest_framework.routers import DefaultRouter

from flats.views import ApartmentViewSet

from booking.views import BookingCreateAPIView, ReservedDatesAPIView

admin.site.site_header = 'Администрирование сайта "Квартиры в Нижнем Новгороде"'
admin.site.site_title = "Администрирование сайта"
admin.site.index_title = "Добро пожаловать!"

router = DefaultRouter()
router.register('apartments', ApartmentViewSet, basename='apartment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/booking/', BookingCreateAPIView.as_view(), name='booking'),
    path('api/dates/<int:apartment_id>/', ReservedDatesAPIView.as_view(), name='apartment-dates'),
    path('api/dates/', ReservedDatesAPIView.as_view(), name='dates'),

    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)