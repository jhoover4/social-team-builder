from django.test import TestCase
from django.urls import reverse

from create_project.models import Project, ProjectPosition, ProjectApplicant
from user_profile.models import CustomUser


class TeamBuilderTestCase(TestCase):
    """
    Tests for general application.
    """

    fixtures = ['initial_data.json']

    def test_index_view(self):
        """
        Should return a valid index view.
        """

        resp = self.client.get(
            reverse('index')
        )

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    def test_index_view_position_data(self):
        """
        Should return an index view with correct position context.
        """

        resp = self.client.get(
            reverse('index')
        )

        projects = Project.objects.all()
        positions = ProjectPosition.objects.filter(project__pk__in=[project.pk for project in projects]).values('name')

        self.assertEqual(len(resp.context['available_positions']), 3)
        self.assertEqual(resp.context['available_positions'][0], positions[0])

    def test_index_view_project_data(self):
        """
        Should return an index view with correct project context.
        """

        resp = self.client.get(
            reverse('index')
        )

        projects = Project.objects.all()

        self.assertEqual(len(resp.context['available_projects']), 2)
        self.assertEqual(resp.context['available_projects'][0], projects[0])

    def test_index_position_filter(self):
        """
        Index should have correct context when URI query string is appended.
        """

        resp = self.client.get(
            reverse('index'),
            {'position': 'iOS Developer'}
        )
        self.assertEqual(resp.context['searched_position'], 'iOS Developer')

    def test_index_position_filter_data(self):
        """
        Should return an index view with correctly filtered project context based on URI query string.
        """

        resp = self.client.get(
            reverse('index'),
            {'position': 'iOS Developer'}
        )

        projects = Project.objects.filter(projectposition__name__iexact='iOS Developer')

        self.assertEqual(len(resp.context['available_projects']), 1)
        self.assertEqual(resp.context['available_projects'][0], projects[0])

    def test_index_search_query(self):
        """
        Should have correct context that matches query search parameter.
        """

        resp = self.client.get(
            reverse('index'),
            {'q': 'Currency Calculator'}
        )

        project = Project.objects.filter(name='Currency Calculator')

        self.assertEqual(resp.context['available_projects'][0], project[0])

    def test_user_notification_data(self):
        """
        Should return an index view with correctly filtered project context based on URI query string.
        """

        test_user = CustomUser.objects.get(pk=2)
        project_position = ProjectPosition.objects.get(pk=1)
        ProjectApplicant.objects.create(user=test_user,
                                        position=project_position,
                                        status='p'
                                        )

        self.client.login(email=test_user.email, password='&Oa0sMqvXJT0')
        resp = self.client.get(
            reverse('index')
        )

        self.assertEqual(len(resp.context['notifications']), 1)
