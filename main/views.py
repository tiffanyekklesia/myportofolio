from django.shortcuts import render
from .models import Experience


def show_main(request):
    context = {
        'name': 'Tiffany Ekklesia',
    }

    return render(request, "index.html", context)


def show_experience(request):
    experiences = Experience.objects.all()

    context = {
        'experiences': experiences,
    }

    return render(request, "experience.html", context)