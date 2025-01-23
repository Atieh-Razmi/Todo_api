from django.urls import path
from . import views
from rest_framework import routers


app_name = 'todo'

urlpatterns =[]

router = routers.SimpleRouter()
router.register('task', views.TaskViewSet)
urlpatterns += router.urls