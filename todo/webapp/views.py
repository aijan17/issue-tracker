from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView, FormView as CustomFormView
from django.views.generic.base import View

from webapp.forms import TaskForm
from webapp.models import Task


class TasksView(TemplateView):
    template_name = 'tasks_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context


class TaskView(TemplateView):
    template_name = 'task_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, id=kwargs.get("id"))
        return context


class AddView(CustomFormView):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'task_add_view.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('tasks_view')
            except:
                form.add_error(None, 'error')
        return render(request, 'task_add_view.html', context={'form': form})


class UpdateView(View):
    def get(self, request, *args, **kwargs):
        task_update = get_object_or_404(Task, id=kwargs.get("id"))
        form = TaskForm(initial={
            'summary': task_update.summary,
            'description': task_update.description,
            'status': task_update.status,
            'types': [t.id for t in task_update.types.all()],
        })
        return render(request, 'update_view.html', context={'form': form, 'id': task_update.id})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        task_update = get_object_or_404(Task, id=kwargs.get("id"))
        if form.is_valid():
            task_update.summary = form.cleaned_data.get('summary')
            task_update.description = form.cleaned_data.get('description')
            task_update.status = form.cleaned_data.get('status')
            task_update.types.set(form.cleaned_data.get('types'))
            task_update.save()
            return redirect('tasks_view')

        return render(request, 'update_view.html', context={'form': form})


class RemoveView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("id"))
        task.delete()
        return redirect('tasks_view')
