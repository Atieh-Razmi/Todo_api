from django.urls import path
from . import views
from rest_framework import routers


app_name = 'todo'

urlpatterns =[
    path('', views.HomeView.as_view(), name='home'),
    path('task/<int:task_id>/', views.Taskdetail.as_view(), name='task_detail'),
]

router = routers.SimpleRouter()
router.register('task', views.TaskViewSet)
urlpatterns += router.urls