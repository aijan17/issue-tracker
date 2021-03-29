from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.views.generic.base import View

from webapp.forms import TaskForm, ProjectForm
from webapp.models import Task, Project


class ProjectListView(ListView):
    model = Project
    template_name = 'home.html'
    queryset = Project.objects.all()
    paginate_by = 3
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        projects = Project.objects.all()

        paginator = Paginator(projects, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            projects_pages = paginator.page(page)
        except PageNotAnInteger:
            projects_pages = paginator.page(1)
        except EmptyPage:
            projects_pages = paginator.page(paginator.num_pages)

        context['lists_pages'] = projects_pages
        return context


class ProjectDetailView(DetailView):
    template_name = 'detail_project.html'
    model = Project
    context_object_name = 'project'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project_task = Project.objects.get(id=self.kwargs.get('pk')).project_task.all()
        paginator = Paginator(project_task, 5)
        page = self.request.GET.get('page')

        try:
            tasks_pages = paginator.page(page)
        except PageNotAnInteger:
            tasks_pages = paginator.page(1)
        except EmptyPage:
            tasks_pages = paginator.page(paginator.num_pages)

        context['lists_pages'] = tasks_pages
        context['is_paginated'] = True
        return context


class ProjectCreateView(CreateView):
    form_class = ProjectForm
    template_name = 'create_project.html'
    queryset = Project.objects.all()
    success_url = reverse_lazy('tasks_view')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class TasksView(ListView):
    model = Task
    template_name = 'tasks_template.html'
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

        context['lists_pages'] = tasks_pages
        return context


class TaskView(DetailView):
    model = Task
    template_name = 'task_template.html'


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
