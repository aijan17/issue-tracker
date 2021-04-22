from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileUpdateForm, PasswordChangeForm
from accounts.models import Profile
from webapp.forms import ProjectUserForm
from webapp.models import Project
from django.views.generic import DetailView

from django.contrib.auth import get_user_model


from django.core.paginator import Paginator



def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('webapp:home')
        else:
            context['has_error'] = True
    return render(request, 'accounts/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:home')


def register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = MyUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('webapp:home')
    else:
        form = MyUserCreationForm()

    return render(request, 'accounts/user_create.html', context={'form': form})


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print(next_url)
        if not next_url:
            next_url = self.request.POST.get('next')
            print(next_url)
        if not next_url:
            next_url = reverse('webapp:home')
            print(next_url)
        return next_url


class UserAdd(PermissionRequiredMixin,UpdateView):
    model = Project
    template_name = 'project/user_project_add.html'
    form_class = ProjectUserForm
    context_object_name = 'user'
    permission_required = ('webapp.add_delete_user',)

    def get_success_url(self):
        return reverse('webapp:home')

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_object'
    paginate_related_by = 3
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        projects = self.get_object().users.all()
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['lists_pages'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class ProfilesList(PermissionRequiredMixin,ListView):
    model = get_user_model()
    template_name = 'accounts/profile_list.html'
    context_object_name = 'profiles'
    paginate_related_by = 3
    paginate_related_orphans = 0
    permission_required = ('accounts.manage_lead',)


class UserChangeView(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'accounts/user_update.html'
    context_object_name = 'user_object'
    profile_form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserChangeView, self).get_context_data(**kwargs)
        context['profile_form'] = kwargs.get('profile_form')
        if context['profile_form'] is None:
            context['profile_form'] = self.get_profile_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = self.get_profile_form()

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        response = super().form_valid(user_form)
        profile_form.save()
        return response

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(form=user_form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return self.profile_form_class(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:user-detail', kwargs={'pk': self.object.pk})


class UserChangePassword(UpdateView):
    model = get_user_model()
    template_name = 'accounts/user_change_pasword.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_object'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super(UserChangePassword, self).form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        return response

    def get_success_url(self):
        return reverse('accounts:user-detail', kwargs={'pk': self.object.pk})


