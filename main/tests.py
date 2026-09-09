from django.test import TestCase
from .models import Experience


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