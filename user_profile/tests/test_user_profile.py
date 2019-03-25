from django.test import TestCase
from django.urls import reverse

from create_project.models import Project, ProjectPosition, ProjectApplicant
from user_profile.models import CustomUser
from user_profile.views import get_all_user_position_applicants


class UserProfileTestCase(TestCase):
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

    def test_view_profile(self):
        """Should be able to see a valid view for viewing a profile."""

        resp = self.client.get(reverse('user_profile:root', kwargs={'profile_id': 1}))

        self.assertTemplateUsed(resp, 'user_profile/profile.html')
        self.assertEqual(resp.status_code, 200)

    def test_view_profile_edit(self):
        """Should be able to see a valid view for editing a profile."""

        resp = self.client.get(reverse('user_profile:edit'))

        self.assertTemplateUsed(resp, 'user_profile/profile_edit.html')
        self.assertEqual(resp.status_code, 200)

    def test_profile_redirect(self):
        """Should be able to redirect to a profile on login."""

        resp = self.client.get(reverse('user_profile:profile_redirect'))
        self.assertEqual(resp.status_code, 302)

    def test_get_all_user_position_applicants(self):
        """Should be able to get all positions user is affiliated with."""

        self.assertEqual(get_all_user_position_applicants(self.test_user2)[0], self.project_applicant)

    def test_get_user_positions_empty(self):
        """Should be able to get all positions user is affiliated with."""

        self.assertFalse(get_all_user_position_applicants(self.test_user))

    def test_view_profile_positions(self):
        """Should be able to see a valid view for viewing a profile."""

        resp = self.client.get(reverse('user_profile:root', kwargs={'profile_id': 2}))

        self.assertTemplateUsed(resp, 'user_profile/profile.html')
        self.assertEqual(resp.context['applications'][0], self.project_applicant)

    def test_view_profile_positions_empty(self):
        """Should be able to see a valid view for viewing a profile."""

        resp = self.client.get(reverse('user_profile:root', kwargs={'profile_id': 1}))

        self.assertTemplateUsed(resp, 'user_profile/profile.html')
        self.assertIsNone(resp.context['applications'])
