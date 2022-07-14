from django.contrib import admin

# Register your models here.
from webapp.models import Task, Type, Status


class TypeInline(admin.TabularInline):
    model = Task.type.through


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'created_at']
    list_display_links = ['summary']
    list_filter = ['status']
    search_fields = ['summary', 'status', 'type']
    fields = ['summary', 'description', 'status', 'created_at', 'updated_at']
    inlines = [TypeInline]
    readonly_fields = ['created_at', 'updated_at']


class TypeAdmin(admin.ModelAdmin):
    inlines = [TypeInline]


admin.site.register(Task, TaskAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Status)
