import re

from django import forms
from django.core.exceptions import ValidationError
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

    def clean_summary(self):
        summary = self.cleaned_data.get("summary")
        if not re.match("^[\w\s]+$", summary):
            raise ValidationError("Заголовок должен состоять из букв или букв с цифрами")
        return summary

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) <= 1:
            raise ValidationError("Описание не должно быть короче двух символов")
        return description


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Найти")