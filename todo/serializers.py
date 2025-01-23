from rest_framework import serializers
from .models import Task
from datetime import datetime


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        if value < datetime.now():
            raise serializers.ValidationError('due_date cannot be in the past')
        return value    