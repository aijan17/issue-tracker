from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from webapp.forms import TaskForm, ProjectForm
from webapp.models import Task, Project


class ProjectListView(ListView):
    model = Project
    template_name = 'project/home.html'
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
    template_name = 'project/detail_project.html'
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


class ProjectCreateView(PermissionRequiredMixin,CreateView):
    form_class = ProjectForm
    template_name = 'project/create_project.html'
    queryset = Project.objects.all()
    success_url = reverse_lazy('webapp:home')
    permission_required = ('webapp.add_project',)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        return super().dispatch(request, *args, **kwargs)


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/update.html'
    form_class = ProjectForm
    context_object_name = 'project'
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse('webapp:home')


class ProjectDeleteView(PermissionRequiredMixin,DeleteView):
    model = Project
    permission_required = ('webapp.delete_project',)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:home')


class TaskView(DetailView):
    model = Task
    template_name = 'task/task_template.html'


class AddView(PermissionRequiredMixin,CreateView):
    form_class = TaskForm
    template_name = 'task/task_add_view.html'
    queryset = Task.objects.all()
    permission_required = ('webapp.add_task',)

    def form_valid(self, form):
        print(form.cleaned_data)
        task = form.save(commit=False)
        task.project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        task.save()
        form.save_m2m()
        return self.get_success_url()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return redirect('webapp:detail', pk= self.kwargs.get('pk'))

    def has_permission(self):
        return super().has_permission() and self.request.user in Project.objects.get(pk=self.kwargs.get('pk')).users.all()


class UpdateViewList(PermissionRequiredMixin,UpdateView):
    form_class = TaskForm
    template_name = 'task/update_view.html'
    permission_required = ('webapp.change_task',)

    def has_permission(self):
        print(self.request.user)
        return super().has_permission() and self.request.user in self.get_object().project.users.all()

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:detail', kwargs={'pk': self.object.project_id})


class RemoveView(PermissionRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('webapp:home')
    permission_required = ('webapp.delete_task',)

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        return super().dispatch(request, *args, **kwargs)



