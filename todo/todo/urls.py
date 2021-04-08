"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from webapp.views import *

from accounts.views import login_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/<int:pk>', TaskView.as_view(), name='task_view'),
    path('add/<int:pk>', AddView.as_view(), name='add_view'),
    path('update/<int:pk>', UpdateViewList.as_view(), name='update_view'),
    path('remove/<int:pk>', RemoveView.as_view(), name='remove_view'),
    path('', ProjectListView.as_view(),name='home'),
    path('detail/<int:pk>', ProjectDetailView.as_view(),name='detail'),
    path('create/', ProjectCreateView.as_view(),name='create'),
    path('delete/<int:pk>',ProjectDeleteView.as_view(),name='delete_project'),
    path('accounts/login',login_view,name='login'),
    path('accounts/logout/', logout_view, name='logout')
]
