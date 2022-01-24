from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage, TaskReorder, CalendarView
from django.contrib.auth.views import LogoutView
from . import views
from .api.api_views import TestTaskDetail, TestTaskList


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('about-us/', views.about, name='about-us'),
    path('projects/', views.projects, name='projects'),
    path('api/test-task/', TestTaskList.as_view(), name='test-task'),
    path('api/test-task/<int:pk>/', TestTaskDetail.as_view()),
]

