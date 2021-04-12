
from django.urls import path
from webapp.views import *

app_name = 'webapp'

urlpatterns = [
path('task/<int:pk>', TaskView.as_view(), name='task_view'),
path('add/<int:pk>', AddView.as_view(), name='add_view'),
path('update/<int:pk>', UpdateViewList.as_view(), name='update_view'),
path('remove/<int:pk>', RemoveView.as_view(), name='remove_view'),
path('', ProjectListView.as_view(), name='home'),
path('detail/<int:pk>', ProjectDetailView.as_view(), name='detail'),
path('create/', ProjectCreateView.as_view(), name='create'),
path('delete/<int:pk>', ProjectDeleteView.as_view(), name='delete_project'),
]