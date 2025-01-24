from rest_framework import serializers
from .models import Task
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'completed', 'created_at', 'updated_at', 'id')

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('due_date cannot be in the past.')
        return value    
    
    def validate(self, data):
        if data['due_date'] < data['created_at']:
            raise serializers.ValidationError("due_date cannot be earlier than created.")
        return data