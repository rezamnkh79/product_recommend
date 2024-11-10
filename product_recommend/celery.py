# myproject/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_recommend.settings')
app = Celery('product_recommend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
