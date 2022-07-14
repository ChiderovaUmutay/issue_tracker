from django import forms
from django.forms import widgets

from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        error_messages = {
            "summary": {
                "required": "Поле обязательно для заполнения"
            },
            "status": {
                "required": "Поле обязательно для заполнения"
            },
        }
        widgets = {
            "type": widgets.CheckboxSelectMultiple
        }