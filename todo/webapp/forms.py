from django import forms
from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('summary', 'description', 'status', 'types')
        widgets = {'types': forms.SelectMultiple(attrs={'class': 'checkbox form-control'}),
                   'description': forms.Textarea(attrs={'cols': 50, 'rows': 10})
                   }




