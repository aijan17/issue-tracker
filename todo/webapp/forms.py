
from django import forms
from django.forms import SelectMultiple, Textarea

from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('summary', 'description', 'status', 'types')
        widgets = {'types':  SelectMultiple(attrs={'class': 'checkbox form-control'}),
                   'description':Textarea(attrs={'class':'form-control'})}