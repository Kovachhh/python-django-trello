from django import forms
from .models import Board, Column, Task
from django.utils.timezone import now

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description']

class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'})
        }

class TaskForm(forms.ModelForm):
    tag = forms.CharField(
        max_length=200, required=False, label="Теги", help_text="Введіть теги через кому."
    )
    assignee = forms.CharField(
        max_length=150, required=False, label="Виконавець"
    )
    author = forms.CharField(
        max_length=150, required=False, label="Автор"
    )

    class Meta:
        model = Task
        fields = ["title", "description", "expired_date", "assignee", "author"]
        widgets = {
            "expired_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_expired_date(self):
        expired_date = self.cleaned_data.get("expired_date")
        if expired_date and expired_date <= now():
            raise forms.ValidationError("Дата закінчення не може бути меншою за сьогоднішню.")
        return expired_date

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        tags = self.cleaned_data.get("tag")
        if tags:
            instance.tags = tags

        assignee_name = self.cleaned_data.get("assignee")
        if assignee_name:
            instance.assignee = assignee_name

        author_name = self.cleaned_data.get("author")
        if author_name:
            instance.author = author_name

        if commit:
            instance.save()
        return instance