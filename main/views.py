import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import HttpResponse

from .models import Experience, Project
from .forms import ProjectForm, ExperienceForm

def show_main(request):
    projects = Project.objects.all()

    last_login = request.COOKIES.get(
        'last_login',
        'Belum ada sesi login / Cookie tidak ditemukan'
    )

    context = {
        'name': 'Tiffany Ekklesia',
        'projects': projects,
        'last_login': last_login,
    }

    return render(request, "index.html", context)


def show_experience(request):
    response = get_experiences_json(request)

    data = serializers.deserialize(
        "json",
        response.content.decode("utf-8")
    )

    experiences = [item.object for item in data]

    context = {
        'experiences': experiences,
    }

    return render(request, "experience.html", context)


def show_projects(request):
    response = get_projects_json(request)

    data = serializers.deserialize(
        "json",
        response.content.decode("utf-8")
    )

    projects = [item.object for item in data]

    context = {
        'projects': projects,
    }

    return render(request, "project.html", context)

@login_required(login_url='/login/')
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('main:show_projects')
    else:
        form = ProjectForm()

    return render(request, "projects_form.html", {'form': form})

@login_required(login_url='/login/')
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.delete()

    return redirect('main:show_projects')

@login_required(login_url='/login/')
def toggle_star(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user in project.stars.all():
        project.stars.remove(request.user)
    else:
        project.stars.add(request.user)

    return redirect('main:show_projects')

def get_projects_json(request):
    name = request.GET.get("name", "").strip()

    if name:
        projects = Project.objects.filter(name__icontains=name)
    else:
        projects = Project.objects.all()

    data = serializers.serialize("json", projects)

    return HttpResponse(
        data,
        content_type="application/json"
    )

def create_experience(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_experience')
    else:
        form = ExperienceForm()

    return render(request, "experiences_form.html", {'form': form})

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)

    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('main:show_experience')
    else:
        form = ExperienceForm(instance=experience)

    return render(request, "experiences_form.html", {'form': form})

def delete_experience(request, experience_id):
    if request.method == "POST":
        experience = get_object_or_404(
            Experience,
            id=experience_id
        )
        experience.delete()

    return redirect('main:show_experience')

def get_experiences_json(request):
    experiences = Experience.objects.all()

    data = serializers.serialize("json", experiences)

    return HttpResponse(
        data,
        content_type="application/json"
    )

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:show_main')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        response = redirect('main:show_main')

        response.set_cookie(
            'last_login',
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        return response

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)

    response = redirect('main:show_main')
    response.delete_cookie('last_login')

    return response