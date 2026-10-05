from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('experience/', views.show_experience, name='show_experience'),
    path(
        'api/experiences/',
        views.get_experiences_json,
        name='get_experiences_json'
    ),
    path('experience/add/', views.create_experience, name='create_experience'),
    path(
        'experience/add-ajax/',
        views.create_experience_ajax,
        name='create_experience_ajax'
    ),
    path(
        'experience/edit/<int:experience_id>/',
        views.update_experience,
        name='update_experience'
    ),
    path(
        'experience/delete/<int:experience_id>/',
        views.delete_experience,
        name='delete_experience'
    ),
    path('projects/', views.show_projects, name='show_projects'),
    path('projects/add/', views.create_project, name='create_project'),
    path(
        'projects/add-ajax/',
        views.create_project_ajax,
        name='create_project_ajax'
    ),
    path(
        'projects/edit/<int:project_id>/',
        views.update_project,
        name='update_project'
    ),
    path('api/projects/', views.get_projects_json, name='get_projects_json'),
    path(
        'projects/delete/<int:project_id>/',
        views.delete_project,
        name='delete_project'
    ),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path(
        'projects/star/<int:project_id>/',
        views.toggle_star,
        name='toggle_star'
    ),
]