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


class ExperiencePageTest(TestCase):
    def test_experience_page_uses_api_and_sets_csrf_cookie(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-list"')
        self.assertContains(response, "/api/v1/experiences/")
        self.assertIn("csrftoken", response.cookies)


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

        page = self.client.get(reverse('main:show_projects'))
        self.assertContains(page, 'id="grid"')

        response = self.client.get(reverse('api:project-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], project.name)
        self.assertEqual(response.data[0]["description"], project.description)
        self.assertEqual(response.data[0]["technologies"], project.technologies)

    def test_empty_state_appears(self):
        response = self.client.get(reverse('main:show_projects'))

        self.assertContains(response, 'No projects yet.')