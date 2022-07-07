from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import TaskForm
from webapp.models import Task


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        tasks = Task.objects.order_by("-updated_at")
        kwargs["tasks"] = tasks
        return super().get_context_data(**kwargs)


class TaskView(TemplateView):
    template_name = "task_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        kwargs["task"] = task
        return super().get_context_data(**kwargs)


class CreateTask(View):
    def get(self, request):
        form = TaskForm()
        return render(request, "create.html", {"form": form})

    def post(self, request):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save()
            return redirect("task_view", pk=new_task.pk)
        return render(request, "create.html", {"form": form})
