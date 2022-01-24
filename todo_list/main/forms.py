from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from calendar import HTMLCalendar

from .models import Task


# Reordering Form and View


class PositionForm(forms.Form):
    position = forms.CharField()


class DateForm(forms.Form):
    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'input-group-append',
            'data-target': '#datetimepicker1',

        })
    )


# renewal_date = forms.DateField()
#
# def clean_renewal_date(self):
#     deadline = self.cleaned_data['renewal_date']
#
#     # Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
#     if deadline < datetime.date.today():
#         raise ValidationError(_('Invalid date - renewal in past'))
#
#     # # Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
#     # if deadline > datetime.date.today() + datetime.timedelta(weeks=4):
#     #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
#
#     # Помните, что всегда надо возвращать "очищенные" данные.
#     return deadline


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.user = user
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, tasks):
        tasks_per_day = tasks.filter(deadline__day=day)
        d = ''
        if tasks_per_day.count() == 0:
            d += ''
        elif tasks_per_day.count() > 1:
            d += 'You have ' + str(tasks_per_day.count()) + " tasks for today"
        else:
            d += 'You have ' + str(tasks_per_day.count()) + " task for today"
        for task in tasks_per_day:
            d += f'<li class="calendar_list"> {task.get_html_url} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, tasks):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, tasks)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        tasks = Task.objects.filter(user=self.user, deadline__year=self.year, deadline__month=self.month)
        cal = f'<table class="calendar" border="0" cellpadding="0" cellspacing="0">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tasks)}\n'
        return cal
