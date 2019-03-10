from django.test import TestCase
from django.urls import reverse

from create_project.models import Project, ProjectPosition, ProjectApplicant
from user_profile.models import CustomUser


class UserDashboardTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=1)
        self.test_user2 = CustomUser.objects.get(pk=2)

        self.test_project = Project.objects.get(pk=1)
        self.project_position = ProjectPosition.objects.get(pk=1)
        self.project_applicant = ProjectApplicant.objects.create(user=self.test_user2,
                                                                 position=self.project_position,
                                                                 status='p'
                                                                 )

        self.client.login(email=self.test_user.email, password='&Oa0sMqvXJT0')

    def test_view_get(self):
        """Should be able to see a valid view for creating a project."""

        resp = self.client.get(reverse('user_profile:user_dashboard', kwargs={'profile_id': 1}))

        self.assertTemplateUsed(resp, 'user_profile/application_dashboard.html')
        self.assertEqual(resp.status_code, 200)

    def test_default_query(self):
        """
        User dashboard with no parameters should return all applications related to user's projects.
        """

        resp = self.client.get(reverse('user_profile:user_dashboard',
                                       kwargs={'profile_id': 1})
                               )
        all_applications = ProjectApplicant.objects.filter(position__project__owner=self.test_user)

        self.assertEqual(resp.context['searched_status'], None)
        self.assertEqual(resp.context['applications'][0], all_applications[0])

    def test_status_query(self):
        """Url param of status should be returned in context."""

        self.project_applicant.status = 'a'
        resp = self.client.get(reverse('user_profile:user_dashboard',
                                       kwargs={'profile_id': 1}) + "?status='a'"
                               )
        self.assertEqual(resp.context['searched_status'], "'a'")

    def test_project_query(self):
        """Url param of project should be returned in context."""

        resp = self.client.get(reverse('user_profile:user_dashboard',
                                       kwargs={'profile_id': 1}) + "?project=Currency+Calculator"
                               )
        self.assertEqual(resp.context['searched_project'], "Currency Calculator")

    def test_job_query(self):
        """Url param of job should be returned in context."""

        resp = self.client.get(reverse('user_profile:user_dashboard',
                                       kwargs={'profile_id': 1}) + "?job=Designer"
                               )
        self.assertEqual(resp.context['searched_job'], "Designer")

    def test_all_queries(self):
        """All relevant url params should be captured."""

        resp = self.client.get(reverse('user_profile:user_dashboard',
                                       kwargs={
                                           'profile_id': 1}) + "?status=a&project=Currency+Calculator&job=Designer"
                               )

        self.assertEqual(resp.context['searched_status'], "a")
        self.assertEqual(resp.context['searched_project'], "Currency Calculator")
        self.assertEqual(resp.context['searched_job'], "Designer")
