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
from .forms import TaskSearchForm
from django.db.models import Q
from django.utils.dateparse import parse_date


# DJANGO CODE
class HomeView(View):
    """
        
    """
    form_class = TaskSearchForm

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


# API CODE
class TaskViewSet(viewsets.ViewSet):
    """
        CREATE, READ, UPDATE, DELETE ON TASKS
    """
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Task.objects.all()
    
    serializer_class = TaskSerializer

    def list(self, request):

        tasks = self.get_queryset()
        due_date = parse_date(request.GET.get("due_date") or "")
        created_at = parse_date(request.GET.get("created_at") or "")

        if due_date:
            tasks = tasks.filter(due_date__date=due_date)
        if created_at:
            tasks = tasks.filter(created_at__date=created_at)

        srz_data = self.serializer_class(instance=tasks, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        task = get_object_or_404(self.get_queryset(), id=pk)
        srz_data = self.serializer_class(instance=task)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        task = get_object_or_404(self.get_queryset(), id=pk)
        srz_data = self.serializer_class(instance=task, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        task = get_object_or_404(self.get_queryset(), id=pk)
        task.delete()
        return Response({'message':'task deleted.'}, status=status.HTTP_200_OK)


# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()  
#     serializer_class = TaskSerializer  

