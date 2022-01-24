from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views import View
from django.shortcuts import redirect
from django.db import transaction
import datetime

from .models import Task
from .forms import PositionForm, DateForm

from .forms import Calendar
from django.utils.html import mark_safe
from datetime import datetime, timezone, timedelta
import calendar
from django.db.models import Q
from django.core.mail import send_mail


class CalendarView(ListView):
    model = Task
    template_name = 'main/calendar.html'
    success_url = reverse_lazy("calendar")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['tasks'] = context['tasks'].filter(user=self.request.user)

        d_obj = get_date(self.request.GET.get('month', None))

        cal = Calendar(d_obj.year, d_obj.month, self.request.user)

        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d_obj)
        context['next_month'] = next_month(d_obj)

        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()


def prev_month(d_obj):
    first = d_obj.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d_obj):
    days_in_month = calendar.monthrange(d_obj.year, d_obj.month)[1]
    last = d_obj.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['tasks'] = context['tasks']
            context['count'] = context['tasks'].filter(complete=False).count()
        else:
            context['tasks'] = context['tasks'].filter(user=self.request.user)
            context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(Q(title__icontains=search_input) | Q(tag__icontains=search_input))
        else:
            return context

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'main/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = {'title', 'description', 'complete', 'deadline', 'tag'}
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)



class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = {'title', 'description', 'complete', 'deadline', 'tag'}
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))


def about(request):
    return render(request, 'main/about-us.html')


def projects(request):
    return render(request, 'main/projects.html')
