from django.test import TestCase
from django.urls import reverse

from create_project.models import ProjectApplicant, ProjectPosition
from user_profile.models import CustomUser


class ProjectApplicantTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=2)
        self.project_position = ProjectPosition.objects.get(pk=1)
        self.project_applicant = ProjectApplicant.objects.create(user=self.test_user,
                                                                 position=self.project_position,
                                                                 status='p'
                                                                 )

        self.client.login(email=self.test_user.email, password='&Oa0sMqvXJT0')

    def test_status_update_view(self):
        """
        Should update applicant status with POST request.
        """

        data = {
            'status': 'r'
        }

        resp = self.client.post(reverse('create_project:applicant_status', kwargs={'pk': self.project_applicant.id}),
                                data=data,
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json)

    def test_status_update_valid_ajax_response(self):
        """
        Updateview should return valid json.
        """

        data = {
            'status': 'r'
        }

        resp = self.client.post(
            reverse('create_project:applicant_status', kwargs={'pk': self.project_applicant.id}),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            {
                'pk': self.project_applicant.id
            },
            resp.json()
        )

    def test_status_update_view_invalid_ajax_response(self):
        """
        Updateview should return valid json and 400 response if AJAX POST invalid.
        """

        data = {
            'status': 'r'
        }

        resp = self.client.post(
            reverse('create_project:applicant_status', kwargs={'pk': self.project_applicant.id}),
            data=data,
        )
        self.assertEqual(
            'Request must be AJAX.',
            resp.json()
        )

    def test_ajax_return_form_errors(self):
        """
        Views should return form errors if data was incorrect.
        """

        data = {
            'status': 'foo'
        }

        error_msg = {'status': ['Select a valid choice. foo is not one of the available choices.']}

        resp = self.client.post(
            reverse('create_project:applicant_status', kwargs={'pk': self.project_applicant.id}),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            error_msg,
            resp.json()
        )

    def test_post_save(self):
        """
        When project applicant is saved and the status has been changed to 'accepted', the project position should be
        marked as filled.
        """

        self.project_position.filled = False

        self.project_applicant.status = 'a'
        self.project_applicant.save()

        self.assertTrue(self.project_position.filled)

    def test_post_save_notifications(self):
        """
        When project applicant is created, it should created a notification object.
        This object will be connected with the user.
        """

        self.assertTrue(hasattr(self.test_user, 'notifications'))

    def test_post_save_multiple_notifications(self):
        """
        When project applicant status changes, new notifications are created for the applicant user.
        This count includes the initial instance creation.
        """

        self.project_applicant.status = 'r'
        self.project_applicant.save()

        self.project_applicant.status = 'p'
        self.project_applicant.save()

        new_notifications = self.test_user.notifications.unread()
        self.assertEqual(len(new_notifications), 3)

    def test_delete(self):
        """
        When project applicant is saved and the status has been changed to 'accepted', the project position should be
        marked as filled.
        """

        data = {
            'pk': self.project_applicant.pk
        }

        resp = self.client.post(
            reverse('create_project:applicant_delete', kwargs={'pk': self.project_applicant.id}),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(resp.status_code, 204)
        self.assertFalse(ProjectApplicant.objects.filter(pk=self.project_applicant.pk).exists())
