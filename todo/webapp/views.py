from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import TemplateView

from webapp.models import Task


class TasksView(TemplateView):
    template_name = 'tasks_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context
