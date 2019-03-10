from django.db.models import OuterRef, Subquery
from django.test import TestCase
from django.urls import reverse

from create_project.models import Project, ProjectApplicant, ProjectPosition
from user_profile.models import CustomUser
from user_profile.models import Skill


class ProjectDetailTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=1)
        self.test_project = Project.objects.get(pk=1)
        self.skill = Skill.objects.get(pk=1)

        self.client.login(email=self.test_user.email, password='&Oa0sMqvXJT0')

    def test_view(self):
        """
        Should return a valid view with correct data.
        """

        resp = self.client.get(
            reverse('create_project:root', kwargs={'pk': self.test_project.pk})
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.test_project, resp.context['project'])
        self.assertTemplateUsed(resp, 'project.html')

    def test_time_involvement_conversion_int(self):
        """
        Should correctly convert minutes to hours for detail view.
        """

        resp = self.client.get(
            reverse('create_project:root', kwargs={'pk': self.test_project.pk})
        )

        self.assertEqual(10, resp.context['project'].time_involvement_hours)

    def test_time_involvement_conversion_float(self):
        """
        Should correctly convert minutes to hours for detail view.
        """

        new_project = Project.objects.create(
            owner=self.test_user,
            name='Test',
            time_involvement=75
        )

        # 75/60 rounded to the 1st decimal should equal 1.2
        time_involvement_hours = 1.2

        resp = self.client.get(
            reverse('create_project:root', kwargs={'pk': new_project.pk})
        )

        self.assertEqual(time_involvement_hours, resp.context['project'].time_involvement_hours)

    def test_user_applied_projects(self):
        """
        Should correctly have amount of projects user has applied to in view.
        """

        user_applied_projects = ProjectApplicant.objects.filter(position=OuterRef('pk'), user=self.test_user)
        project_positions = ProjectPosition.objects.filter(project__id=self.test_project.id).annotate(
            user_applied=Subquery(user_applied_projects.values('id'))).order_by('pk')

        resp = self.client.get(
            reverse('create_project:root', kwargs={'pk': self.test_project.pk})
        )

        self.assertEqual(list(resp.context['project_positions']), list(project_positions))

    def test_user_applied_projects_empty(self):
        """
        Should have None in context if there are no user applied projects.
        """

        new_project = Project.objects.create(
            owner=self.test_user,
            name='Test',
            time_involvement=75
        )

        resp = self.client.get(
            reverse('create_project:root', kwargs={'pk': new_project.pk})
        )

        self.assertFalse(resp.context['project_positions'].exists())
