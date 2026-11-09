from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            name="Portfolio", description="My website", technologies="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "name": "New project", "description": "A useful app",
            "technologies": "Python", "project_url": "https://example.com/",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.project.id)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"name": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"name": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[999999])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"name": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="experience-owner",
            email="experience-owner@example.com",
            password="test-owner-password",
        )
        self.visitor = User.objects.create_user(
            username="experience-visitor",
            password="test-visitor-password",
        )
        self.editor = User.objects.create_user(
            username="experience-editor",
            password="test-editor-password",
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(self.editor_group)
        self.experience = Experience.objects.create(
            title="Software Engineer",
            company="Example Co",
            description="Built useful software.",
            start_date="2024-01-01",
            end_date=None,
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.pk],
        )
        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.pk],
        )
        self.payload = {
            "title": "Product Designer",
            "company": "New Company",
            "description": "Designed useful products.",
            "start_date": "2025-01-01",
            "end_date": None,
        }

    def test_public_read_and_search(self):
        response = self.client.get(self.list_url, {"search": "engineer"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.experience.pk)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("stars", response.data[0])

        missing = self.client.get(self.list_url, {"search": "not found"})
        self.assertEqual(missing.data, [])
        detail = self.client.get(self.detail_url)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_missing_experience_returns_404(self):
        response = self.client.get(
            reverse("api:experience-detail", args=[999999])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_and_regular_users_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            create_response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )
            patch_response = self.client.patch(
                self.detail_url,
                {"title": "Changed"},
                format="json",
            )
            delete_response = self.client.delete(self.detail_url)

            self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(Experience.objects.count(), 1)
            self.experience.refresh_from_db()
            self.assertEqual(self.experience.title, "Software Engineer")

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        patch_response = self.client.patch(
            self.detail_url,
            {"title": "Updated by editor"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated by editor")

        create_response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        delete_response = self.client.delete(self.detail_url)
        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        create_response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        created_id = create_response.data["id"]
        self.assertTrue(Experience.objects.filter(pk=created_id).exists())

        delete_response = self.client.delete(
            reverse("api:experience-detail", args=[created_id])
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=created_id).exists())

    def test_serializer_validation_and_html_stripping(self):
        self.client.force_authenticate(user=self.owner)
        invalid_response = self.client.post(
            self.list_url,
            {**self.payload, "title": "   "},
            format="json",
        )
        self.assertEqual(
            invalid_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("title", invalid_response.data)
        self.assertEqual(Experience.objects.count(), 1)

        sanitized_response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "title": "  <b>Product Designer</b>  ",
                "company": "<i>New Company</i>",
                "description": "<p>Designed useful products.</p>",
            },
            format="json",
        )
        self.assertEqual(
            sanitized_response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(sanitized_response.data["title"], "Product Designer")
        self.assertEqual(sanitized_response.data["company"], "New Company")
        self.assertEqual(
            sanitized_response.data["description"],
            "Designed useful products.",
        )

    def test_star_requires_login_and_toggles_for_regular_user(self):
        anonymous_response = self.client.post(self.star_url)
        self.assertEqual(
            anonymous_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(self.experience.stars.count(), 0)

        self.client.force_authenticate(user=self.visitor)
        first_response = self.client.post(self.star_url)
        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertTrue(first_response.data["is_starred"])
        self.assertEqual(first_response.data["star_count"], 1)

        second_response = self.client.post(self.star_url)
        self.assertFalse(second_response.data["is_starred"])
        self.assertEqual(second_response.data["star_count"], 0)
        self.assertEqual(self.experience.stars.count(), 0)

    def test_session_write_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(
            client.login(
                username="experience-owner",
                password="test-owner-password",
            )
        )
        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)


class ProjectAPITailTests(APITestCase):
    def setUp(self):
        ProjectAPITest.setUp(self)

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"name": "   "}, "name"),
            ({"name": '<img src="x" onerror="alert(1)">'}, "name"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"name": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"name": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"name": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)