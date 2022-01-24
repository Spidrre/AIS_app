from django import template
from datetime import datetime, timezone
import pytz

register = template.Library()
now = datetime.now(timezone.utc)


@register.simple_tag()
def my_tag(task):
    timezone = pytz.timezone("UTC")
    time_now = timezone.localize(datetime.today())
    deadline_time = task.deadline

    diffTime = abs(time_now - deadline_time)

    flag = False
    if time_now < deadline_time:
        flag = False
    else:
        flag = True

    return {"flag": flag, "time": diffTime}
