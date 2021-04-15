from django import forms

from webapp.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('summary', 'description', 'status', 'types')
        widgets = {'types': forms.SelectMultiple(attrs={'class': 'checkbox form-control'}),
                   'description': forms.Textarea(attrs={'cols': 50, 'rows': 10})
                   }


class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'desc', 'begin_date', 'expiration_date')
        widgets = {
            'begin_date': DateInput(),
            'expiration_date': DateInput()
        }


class ProjectUserForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('users',)
        widgets = {'users': forms.SelectMultiple(attrs={'class': 'checkbox form-control'}),}
