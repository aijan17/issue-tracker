from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

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
        project = Project.objects.get(id=self.kwargs.get('pk'))
        project_task = project.tasks.all()
        page = self.request.GET.get('page')

        query = self.request.GET.get('q', None)
        if query is not None:
            project_task = project_task.filter(
                Q(summary__icontains=query) |
                Q(description__icontains=query)
            )

        paginator = Paginator(project_task, 5)

        try:
            tasks_pages = paginator.page(page)
        except PageNotAnInteger:
            tasks_pages = paginator.page(1)
        except EmptyPage:
            tasks_pages = paginator.page(paginator.num_pages)

        context['lists_pages'] = tasks_pages
        context['project'] = project
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


class ProjectDeleteView(DeleteView):
    model = Project

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')


class TaskView(DetailView):
    model = Task
    template_name = 'task_template.html'


class AddView(CreateView):
    form_class = TaskForm
    template_name = 'task_add_view.html'
    queryset = Task.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        form.project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.kwargs.get('pk')})


class UpdateViewList(UpdateView):
    form_class = TaskForm
    template_name = 'update_view.html'

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.project_id})


class RemoveView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks_view')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)




