from django import forms
from .models import Task



class TaskSearchForm(forms.Form):
    search = forms.CharField()