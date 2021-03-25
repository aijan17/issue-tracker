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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TasksView.as_view(), name='tasks_view',),
    path('task/<int:pk>', TaskView.as_view(), name='task_view'),
    path('add/', AddView.as_view(), name='add_view'),
    path('update/<int:pk>', UpdateViewList.as_view(), name='update_view'),
    path('remove/<int:pk>', RemoveView.as_view(), name='remove_view'),
]
