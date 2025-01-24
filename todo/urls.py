from django.urls import path
from . import views
from rest_framework import routers


app_name = 'todo'

urlpatterns =[
    #HTML
    #path('', views.HomeView.as_view(), name='home'),
    #path('task/<int:task_id>/', views.Taskdetail.as_view(), name='task_detail'),
]
#API
router = routers.SimpleRouter()
router.register('task', views.TaskViewSet, basename='task')
urlpatterns += router.urls