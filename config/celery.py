import os

from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)


app = Celery(   # Creates our task manager.
    "clinic"
)


app.config_from_object(  # celery reads : REDIS URL, timezone, task settings
    "django.conf:settings",
    namespace="CELERY"
)


app.autodiscover_tasks() # Look inside apps for: tasks.py e.g. in appointments app