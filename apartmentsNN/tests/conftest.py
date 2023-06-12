from django.conf import settings

import backend.settings as apartmentsNN_settings


def pytest_configure():
    settings.configure(
        DEBUG=apartmentsNN_settings.DEBUG,
        SECRET_KEY = apartmentsNN_settings.SECRET_KEY,
        INSTALLED_APPS=apartmentsNN_settings.INSTALLED_APPS,
        DATABASES=apartmentsNN_settings.DATABASES,
        EMAIL_BACKEND=apartmentsNN_settings.EMAIL_BACKEND,
        ROOT_URLCONF='backend.urls',
        REST_FRAMEWORK={
            'TEST_REQUEST_DEFAULT_FORMAT': 'json',
        }
    )
