"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from tasks import views
from django.conf.urls.static import static 
from django.conf import settings 
from tasks.views import TeamListView,TeamCreateView,TeamUpdateView,TeamDeleteView,TaskListView,TaskCreateView,TaskUpdateView,TaskDeleteView,MyTaskListView,TaskMemberUpdateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),

    path('teams/', TeamListView.as_view(), name='team_list'),
    path('create_team/', TeamCreateView.as_view(), name='create_team'),
    path('edit_team/<int:pk>/', TeamUpdateView.as_view(), name='edit_team'),
    path('delete_team/<int:pk>/', TeamDeleteView.as_view(), name='delete_team'),


    path('task_list/', TaskListView.as_view(), name='task_list'),
    path('create_task/', TaskCreateView.as_view(), name='create_task'),
    path('update_task/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete_task/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),

    path('my_task_list/', MyTaskListView.as_view(), name='my_task_list'),
    path('my_update_task/<int:pk>/', TaskMemberUpdateView.as_view(), name='my_update_task'),

   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
