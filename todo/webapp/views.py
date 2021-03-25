from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.views.generic.base import View

from webapp.forms import TaskForm
from webapp.models import Task


class TasksView(ListView):
    model = Task
    template_name = 'tasks_template.html'
    context_object_name = 'tasks'
    ordering = ('summary', '-create_date')
    paginate_by = 10
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)
        tasks = Task.objects.all()

        query = self.request.GET.get('q', None)
        if query is not None:
            tasks = tasks.filter(
                Q(summary__icontains=query) |
                Q(description__icontains=query)
            )

        paginator = Paginator(tasks, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            tasks_pages = paginator.page(page)
        except PageNotAnInteger:
            tasks_pages = paginator.page(1)
        except EmptyPage:
            tasks_pages = paginator.page(paginator.num_pages)

        context['tasks'] = tasks_pages
        return context


class TaskView(DetailView):
    model = Task
    template_name = 'task_template.html'

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Task, id=id_)


class AddView(CreateView):
    form_class = TaskForm
    template_name = 'task_add_view.html'
    queryset = Task.objects.all()
    success_url = reverse_lazy('tasks_view')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UpdateViewList(UpdateView):
    form_class = TaskForm
    template_name = 'update_view.html'
    success_url = reverse_lazy('tasks_view')

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class RemoveView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("pk"))
        task.delete()
        return redirect('tasks_view')
