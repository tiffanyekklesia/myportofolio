from django.test import TestCase
from django.urls import reverse
from .models import Experience, Project


class ExperienceModelTest(TestCase):
    def test_experience_creation(self):
        experience = Experience.objects.create(
            title="Test Experience",
            company="Test Company",
            description="This is a test experience.",
            start_date="2026-01-01",
            end_date=None
        )

        self.assertEqual(experience.title, "Test Experience")
        self.assertEqual(experience.company, "Test Company")
        self.assertIsNone(experience.end_date)

class ProjectPageTest(TestCase):
    def test_projects_page_url_and_template(self):
        response = self.client.get(reverse('main:show_projects'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project.html')

    def test_project_data_appears(self):
        project = Project.objects.create(
            name="Test Project",
            description="Test description",
            technologies="Python"
        )

        response = self.client.get(reverse('main:show_projects'))

        self.assertContains(response, project.name)
        self.assertContains(response, project.description)
        self.assertContains(response, project.technologies)

    def test_empty_state_appears(self):
        response = self.client.get(reverse('main:show_projects'))

        self.assertContains(response, 'No projects yet.')