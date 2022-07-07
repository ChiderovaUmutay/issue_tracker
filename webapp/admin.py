from django.contrib import admin

# Register your models here.
from webapp.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'created_at']
    list_display_links = ['summary']
    list_filter = ['status']
    search_fields = ['summary', 'status', 'type']
    fields = ['summary', 'description', 'status', 'type', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)
