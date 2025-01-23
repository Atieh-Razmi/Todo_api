from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.views import APIView
from .models import Task
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.views import View
from .forms import TaslSearchForm
from django.db.models import Q
# Create your views here.

class HomeView(View):
    form_class = TaslSearchForm

    def get(self, request):
        tasks = Task.objects.all()
        search_query = request.GET.get('search')
        if search_query:
            tasks = tasks.filter(Q(title__icontains=request.GET['search']) | 
                                 Q(description__icontains=request.GET['search']))
        return render(request, 'todo/home.html', {'tasks':tasks, 'form':self.form_class})
    
class Taskdetail(View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        return render(request, 'todo/detail.html', {'task':task})    



class TaskViewSet(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated,]
    queryset = Task.objects.all()

    def list(self, request):
        srz_data = TaskSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        ser_data = TaskSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        task = get_object_or_404(self.queryset, id=pk)
        srz_data = TaskSerializer(instance=task)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        task = get_object_or_404(self.queryset, id=pk)
        srz_data = TaskSerializer(instance=task, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        task = get_object_or_404(self.queryset, id=pk)
        task.delete()
        return Response({'message':'task deleted.'}, status=status.HTTP_200_OK)

