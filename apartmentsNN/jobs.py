#!/usr/local/bin python
import datetime as dt

from scheduler import Scheduler

import environ

import django
from django.conf import settings
from backend.settings import EMAIL_BACKEND, INSTALLED_APPS, LOGGING
# print(LOGGING)
# from apartmentsNN import diffset as myapp_defaults
#
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)

settings.configure(
    DEBUG=env("DEBUG"),
    INSTALLED_APPS=INSTALLED_APPS,
    LOGGING=LOGGING,
    EMAIL_BACKEND=EMAIL_BACKEND,
    DATABASES={
        'default': {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB", default=""),
            "USER": env("POSTGRES_USER", default=""),
            "PASSWORD": env("POSTGRES_PASSWORD", default=""),
            "HOST": env("POSTGRES_HOST", default="localhost"),
            "PORT": env("POSTGRES_PORT", cast=int, default=5432),
            # "PORT": 5432,
            # "ATOMIC_REQUESTS": True,
        }
    },
)
django.setup()


def foo():
    from django.core import management
    from booking.management.commands import cancel_booking

    management.call_command('cancel_booking')


schedule = Scheduler()
schedule.minutely(dt.time(second=15), foo)

# print(schedule)
# import time

schedule.exec_jobs(force_exec_all=True)

# print(schedule)

# time.sleep(1)
