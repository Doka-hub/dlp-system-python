from celery import Celery

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dlp_system.settings')


celery_app = Celery('app', result_expires=60)
celery_app.config_from_object('django.conf:settings')

celery_app.autodiscover_tasks()
