import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

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
    context = {
        'form': ExperienceForm(),
    }

    return render(request, "experience.html", context)

def show_projects(request):
    context = {
        'name': 'Tiffany Ekklesia',
        'title_query': request.GET.get('name', '').strip(),
        'form': ProjectForm(),
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

@require_POST
@login_required(login_url='/login/')
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {'error': 'You do not have permission to create projects.'},
            status=403
        )

    form = ProjectForm(request.POST)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()

        return JsonResponse(
            {
                'message': 'Project created successfully.',
                'project_id': project.id,
            },
            status=201
        )

    return JsonResponse(
        {
            'errors': form.errors,
        },
        status=400
    )

@login_required(login_url='/login/')
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not (
        request.user.is_superuser
        or request.user.has_perm('main.change_project')
    ):
        raise PermissionDenied

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('main:show_projects')
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "projects_form.html",
        {
            'form': form,
            'is_edit': True,
        }
    )

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

    if request.method == "POST":
        if request.user in project.stars.all():
            project.stars.remove(request.user)
        else:
            project.stars.add(request.user)

    return redirect('main:show_projects')

def get_projects_json(request):
    name_query = request.GET.get("name", "").strip()

    projects = Project.objects.prefetch_related('stars').all()

    if name_query:
        projects = projects.filter(name__icontains=name_query)

    data = []

    for project in projects:
        starred_users = project.stars.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [user.username for user in starred_users]
        )

        data.append({
            "pk": str(project.id),
            "fields": {
                "name": project.name,
                "description": project.description,
                "technologies": project.technologies,
                "project_url": project.project_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def create_experience(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_experience')
    else:
        form = ExperienceForm()

    return render(request, "experiences_form.html", {'form': form})

@require_POST
def create_experience_ajax(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse(
            {
                'error': 'You do not have permission to create experiences.'
            },
            status=403
        )

    form = ExperienceForm(request.POST)

    if form.is_valid():
        experience = form.save()

        return JsonResponse(
            {
                'message': 'Experience created successfully.',
                'experience_id': experience.id,
            },
            status=201
        )

    return JsonResponse(
        {
            'errors': form.errors,
        },
        status=400
    )

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
    search_query = request.GET.get("search", "").strip()

    experiences = Experience.objects.prefetch_related('stars').all()

    if search_query:
        experiences = experiences.filter(
            title__icontains=search_query
        )

    data = []

    for experience in experiences:
        starred_users = experience.stars.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        data.append({
            "id": experience.id,
            "title": experience.title,
            "company": experience.company,
            "description": experience.description,
            "start_date": experience.start_date.strftime("%Y-%m-%d"),
            "end_date": (
                experience.end_date.strftime("%Y-%m-%d")
                if experience.end_date
                else None
            ),
            "star_count": starred_users.count(),
            "is_starred": is_starred,
        })

    return JsonResponse(data, safe=False)

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