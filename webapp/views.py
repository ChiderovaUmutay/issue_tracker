from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from webapp.forms import TaskForm, SearchForm
from webapp.models import Task


class IndexView(ListView):
    model = Task
    template_name = "index.html"
    context_object_name = "tasks"
    ordering = ("-updated_at",)
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")

    def get_queryset(self):
        if self.search_value:
            return Task.objects.filter(
                Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({"search": self.search_value})
            context["query"] = query
            context["search"] = self.search_value
        return context


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


class UpdateTask(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.task = get_object_or_404(Task, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TaskForm(initial={
            "summary": self.task.summary,
            "description": self.task.description,
            "status": self.task.status,
            "type": self.task.type.all(),
        })
        return render(request, "update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            self.task.summary = form.cleaned_data.get("summary")
            self.task.description = form.cleaned_data.get("description")
            self.task.status = form.cleaned_data.get("status")
            self.task.type.set(form.cleaned_data.pop("type"))
            self.task.save()
            return redirect("task_view", pk=self.task.pk)
        return render(request, "update.html", {"form": form})


class DeleteTask(View):
    def post(self, request, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect("index")
