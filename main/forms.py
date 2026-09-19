from django.forms import ModelForm
from main.models import Project, Experience


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'technologies', 'project_url']

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'description', 'start_date', 'end_date']