from celery import shared_task

from .models import Timetable # модель для тикетов


@shared_task
def add_inf_to_timetable():
    c = Timetable(days_of_the_week='Wednesday', task='1 person')
    c.save()