#!/usr/local/bin python

import datetime as dt
import time

from scheduler import Scheduler
import django
from django.conf import settings

import backend.settings as apartmentsNN_settings

settings.configure(
    DEBUG=apartmentsNN_settings.DEBUG,
    INSTALLED_APPS=apartmentsNN_settings.INSTALLED_APPS,
    DATABASES = apartmentsNN_settings.DATABASES,
    LOGGING=apartmentsNN_settings.LOGGING,
    EMAIL_BACKEND=apartmentsNN_settings.EMAIL_BACKEND,
)
django.setup()


def cancel_booking_job():
    from django.core import management
    management.call_command('cancel_booking')


schedule = Scheduler()
schedule.hourly(dt.time(minute=30), cancel_booking_job)

# print(schedule)
# schedule.exec_jobs(force_exec_all=True)

while True:
    schedule.exec_jobs()
    time.sleep(3600)
