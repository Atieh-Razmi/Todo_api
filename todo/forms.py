from django import forms
from .models import Task

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ["title", "completed"]

class TaslSearchForm(forms.Form):
    search = forms.CharField()