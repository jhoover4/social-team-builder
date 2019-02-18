import json

from django.test import TestCase
from django.urls import reverse

from create_project.models import Project, ProjectApplicant, ProjectPosition
from user_profile.models import CustomUser
from user_profile.models import Skill
from .forms import ProjectForm, ProjectFormSet


class ProjectTestCase(TestCase):
    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=1)
        self.test_project = Project.objects.get(pk=1)
        self.skill = Skill.objects.get(pk=1)

        self.client.login(email=self.test_user.email, password='&Oa0sMqvXJT0')

    def test_project_detail_view(self):
        """
        Should return a valid view with correct data.
        """

        resp = self.client.get(
            reverse('create_project:root', kwargs={'pk': self.test_project.pk})
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.test_project, resp.context['project'])
        self.assertTemplateUsed(resp, 'project.html')

    def test_project_detail_view_time_involvement_conversion_int(self):
        """
        Should correctly convert minutes to hours for detail view.
        """

        resp = self.client.get(
            reverse('create_project:root', kwargs={'pk': self.test_project.pk})
        )

        self.assertEqual(10, resp.context['project'].time_involvement_hours)

    def test_project_detail_view_time_involvement_conversion_float(self):
        """
        Should correctly convert minutes to hours for detail view.
        """

        test_project2 = Project.objects.create(
            owner=self.test_user,
            name='Test',
            time_involvement=75
        )

        # 75/60 rounded to the 1st decimal should equal 1.2
        time_involvement_hours = 1.2

        resp = self.client.get(
            reverse('create_project:root', kwargs={'pk': test_project2.pk})
        )

        self.assertEqual(time_involvement_hours, resp.context['project'].time_involvement_hours)

    def test_create_project_view(self):
        """
        Should be able to see a valid view for creating a project.
        """

        resp = self.client.get(reverse('create_project:new'))
        self.assertTemplateUsed(resp, 'project_create_edit.html')

    def test_edit_project_view(self):
        """
        Should be able to see a valid view for editing a project.
        """

        resp = self.client.get(reverse('create_project:edit', kwargs={'pk': self.test_project.pk}))
        self.assertTemplateUsed(resp, 'project_create_edit.html')

    def test_project_form(self):
        """
        Should be able to use a valid form to submit data to edit or create a project.
        """
        form_data = {'owner': self.test_user.id,
                     'name': 'test',
                     'description': 'test',
                     'time_involvement': 65,
                     'applicant_requirements': 'test'
                     }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_project_formset(self):
        """
        Should be able to use a valid form to submit data to edit or create a project.
        """
        form_data = {'owner': self.test_user.id,
                     'name': 'test',
                     'description': 'test',
                     'time_involvement': '65',
                     'applicant_requirements': 'test',

                     # Management form data
                     'projectposition_set-TOTAL_FORMS': '2',
                     'projectposition_set-INITIAL_FORMS': '0',
                     'projectposition_set-MAX_NUM_FORMS': '',

                     # First position data
                     'projectposition_set-0-name': 'Test',
                     'projectposition_set-0-description': 'test description',
                     'projectposition_set-0-related_skills': [self.skill],
                     'projectposition_set-0-time_involvement': '60',

                     # Second position data
                     'projectposition_set-1-name': 'Test2',
                     'projectposition_set-1-description': 'test2 description',
                     'projectposition_set-1-related_skills': [self.skill],
                     'projectposition_set-1-time_involvement': '115',
                     }

        formset = ProjectFormSet(data=form_data)
        self.assertTrue(formset.is_valid())

    def test_edit_project_view_post(self):
        """
        Post to create a new project should return a redirect and create a new object.
        """

        form_data = {'name': 'test',
                     'description': 'test',
                     'time_involvement': '65',
                     'applicant_requirements': 'test',

                     # Management form data
                     'projectposition_set-INITIAL_FORMS': '0',
                     'projectposition_set-TOTAL_FORMS': '2',
                     'projectposition_set-MAX_NUM_FORMS': '',

                     # First position data
                     'projectposition_set-0-title': 'Test',
                     'projectposition_set-0-description': 'test description',

                     # Second position data
                     'projectposition_set-1-title': 'Test2',
                     'projectposition_set-1-description': 'test2 description',
                     }

        resp = self.client.post(reverse('create_project:new'), form_data)
        self.assertEqual(resp.status_code, 302)

        new_project = Project.objects.latest('pk')
        self.assertEqual('test', new_project.name)


class ProjectApplicantTestCase(TestCase):
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
            'id': self.project_applicant.id,
            'status': 'r'
        }

        resp = self.client.post(reverse('create_project:applicant_status', kwargs={'pk': self.project_applicant.id}),
                                data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json)

    def test_status_update_valid_ajax_response(self):
        """
        Updateview should return valid json.
        """

        data = json.dumps({
            'id': self.project_applicant.id,
            'status': 'r'
        })

        resp = self.client.post(
            reverse('create_project:applicant_status', kwargs={'pk': self.project_applicant.id}),
            content_type='application/json',
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            'Success',
            resp.json()
        )

    def test_status_update_view_invalid_ajax_response(self):
        """
        Updateview should return valid json and 400 response if AJAX POST invalid.
        """

        data = json.dumps({
            'id': self.project_applicant.id,
            'status': 'r'
        })

        resp = self.client.post(
            reverse('create_project:applicant_status', kwargs={'pk': self.project_applicant.id}),
            content_type='application/json',
            data=data,
        )
        self.assertEqual(
            'Request must be AJAX.',
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
