import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dellin_work.settings')
app = Celery('dellin_work')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'notification_listeners_lessons': {
    #     'task': 'lesson.tasks.notification_listeners_lessons',
    #     'schedule': crontab(hour='5, 6, 7, 8, 9, 10, 11, 12, 13, 14, '
    #                              '15, 16, 17, 18, 19, 20, 21, 22, 23',
    #                         minute='0, 15, 30, 45'),
    # },
    # 'notification_tomorrow_schedule': {
    #     'task': 'lesson.tasks.notification_tomorrow_schedule',
    #     'schedule': crontab(hour='20', minute='0')
    # },
    # 'notification_listeners_tomorrow_lessons': {
    #     'task': 'lesson.tasks.notification_listeners_tomorrow_lessons',
    #     'schedule': crontab(hour='5, 6, 7, 8, 9, 10, 11, 12, 13, 14, '
    #                              '15, 16, 17, 18, 19, 20, 21, 22, 23',
    #                         minute='0')
    # }
}
