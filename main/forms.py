from django.forms import ModelForm
from django.utils.html import strip_tags
from main.models import Project, Experience


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'technologies', 'project_url']


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'description', 'start_date', 'end_date']

    def clean_title(self):
        title = self.cleaned_data['title']
        return strip_tags(title).strip()

    def clean_company(self):
        company = self.cleaned_data['company']
        return strip_tags(company).strip()

    def clean_description(self):
        description = self.cleaned_data['description']
        return strip_tags(description).strip()