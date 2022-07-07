from django.urls import path

from webapp.views import IndexView, TaskView, CreateTask, UpdateTask

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/view', TaskView.as_view(), name='task_view'),
    path('tasks/add/', CreateTask.as_view(), name='create_task'),
    path('task/<int:pk>/update', UpdateTask.as_view(), name='update_task'),
]
