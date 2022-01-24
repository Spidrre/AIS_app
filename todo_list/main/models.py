from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .templatetags.time_tag import my_tag


class Testtask(models.Model):
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=100,default="none")

    def printt(self):
        return f"i'm {self.number} {self.title}"


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField('Name', max_length=100)
    description = models.TextField('Description', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now_add=False, editable=True)
    complete = models.BooleanField(default=False)
    tag = models.CharField('Tag', null=True, blank=True, max_length=50)

    def __str__(self):
        return self.title

    def printt(self):
        return f'Title: {self.title}, Description: {self.description}'

    def printd(self):
        return f'Deadline: {self.deadline}'

    @property
    def get_html_url(self):
        url = reverse('task-update', args=(self.id,))
        val = my_tag(self)
        if self.complete:
            return f'<i><s>{self.title}&#160;</i></s>'
        else:
            if val['flag']:
                return f'<p style="font-size:12px; color: #c8070a;">{self.title}&#160;<a href="{url}">edit</a></p>'
            else:
                return f'<p style="font-size:12px; color: #0ad30a;">{self.title}&#160;<a href="{url}">edit</a></p>'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        order_with_respect_to = 'user'
