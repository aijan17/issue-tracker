from django.urls import path

from accounts.views import login_view, logout_view, register_view, RegisterView, UserAdd, UserDetailView, ProfilesList

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('create/', RegisterView.as_view(), name='create'),
    path('add/user/<int:pk>/',UserAdd.as_view(),name='add-user'),
    path('user/deteil/<int:pk>',UserDetailView.as_view(),name='user-detail'),
    path('profiles',ProfilesList.as_view(),name='profile')

]
