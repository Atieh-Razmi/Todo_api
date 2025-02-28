from django.contrib import admin
from .models import Task
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'due_date')
    search_fields = ('title',)
    list_filter = ('updated_at',)





