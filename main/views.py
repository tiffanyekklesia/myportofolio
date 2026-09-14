from django.shortcuts import render
from .models import Experience, Project


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
    projects = Project.objects.all()

    context = {
        'projects': projects,
    }

    return render(request, "project.html", context)