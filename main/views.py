from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from .models import Experience, Project
from .forms import ProjectForm

def show_main(request):
    projects = Project.objects.all()

    context = {
        'name': 'Tiffany Ekklesia',
        'projects': projects,
    }

    return render(request, "index.html", context)


def show_experience(request):
    experiences = Experience.objects.all()

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

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_projects')
    else:
        form = ProjectForm()

    return render(request, "projects_form.html", {'form': form})

def delete_project(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        project.delete()

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