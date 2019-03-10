from django.test import TestCase
from django.urls import reverse

from create_project.models import Project, ProjectPosition


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
