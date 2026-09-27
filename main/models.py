from django.db import models
from django.contrib.auth.models import User

class Experience(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    project_url = models.URLField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    stars = models.ManyToManyField(User, related_name='starred_projects', blank=True)

    def __str__(self):
        return self.name