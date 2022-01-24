from django.urls import path

#from .api_views import AstroMapListAPIView
from .api_views import testTaskDetail, testTaskList


urlpatterns = [
    path('test-task/', testTaskList.as_view(), name='test-task'),
    path('test-task/<int:pk>/', testTaskDetail.as_view()),
]