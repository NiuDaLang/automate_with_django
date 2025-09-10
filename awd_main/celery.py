import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awd_main.settings')

# Sets up the new celery application for our Django project "awd_main"
app = Celery('awd_main')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
# By default Celery looks for the module named [task.py] in your Django apps 
# and registers the tasks defined in those modules. 
app.autodiscover_tasks()

# Debug task
# task decorator to inform celery that the function below it should be gtreated
# as an asynchronous task that can be scheduled and executed in the backgtound.
# [bind=True] => you are giving your celery task fn the ability to interact 
# with the info about the task itself while it is still running.
# [ignore_result=True] => tells celery that don't store the result in the result backend.
# 
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')