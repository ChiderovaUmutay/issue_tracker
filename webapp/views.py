from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from webapp.models import Task


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        tasks = Task.objects.order_by("-status")
        kwargs["tasks"] = tasks
        return super().get_context_data(**kwargs)