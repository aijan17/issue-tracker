
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from accounts.forms import MyUserCreationForm
from webapp.forms import ProjectUserForm
from webapp.models import Project



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


class UserAdd(UpdateView):
    model = Project
    template_name = 'project/user_project_add.html'
    form_class = ProjectUserForm
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('webapp:home')

