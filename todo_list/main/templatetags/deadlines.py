from django import template
from ..models import Task
import datetime


register = template.Library()


@register.simple_tag()
def tasks_for_day(deadline):
    format = '%Y-%m-%d %H:%M'
    d1 = datetime.datetime.strftime(deadline,format)
    list = Task.objects.filter(deadline__date=d1)
    return list.count