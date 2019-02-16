from django.test import TestCase
from django.urls import reverse

from create_project.models import Project, ProjectApplicant, ProjectPosition
from user_profile.models import CustomUser
from .forms import ProjectForm, ProjectFormSet
from user_profile.models import Skill


class ProjectTestCase(TestCase):
    def setUp(self):
        self.test_user = CustomUser.objects.create(
            first_name='Jordan',
            last_name='Hoover',
            email='jordan@hoovermld.com'
        )
        self.test_project = Project.objects.create(
            owner=self.test_user,
            name='Currency Calculator',
            description='test',
            time_involvement=60,
            applicant_requirements='Applicants are required to work from our headquarters located in Antarctica.'
        )
        self.skill = Skill.objects.create(name='Python')

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

        self.assertEqual(1, resp.context['project'].time_involvement_hours)

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
        self.assertTemplateUsed(resp, 'project_edit.html')

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
        form_data = {'name': 'test',
                     'description': 'test',
                     'time_involvement': '65',
                     'applicant_requirements': 'test',

                     # Management form data
                     'projectposition-INITIAL_FORMS': '0',
                     'projectposition-TOTAL_FORMS': '2',
                     'projectposition-MAX_NUM_FORMS': '',

                     # First position data
                     'projectposition-0-title': 'Test',
                     'projectposition-0-description': 'test description',

                     # Second position data
                     'projectposition-1-title': 'Test2',
                     'projectposition-1-description': 'test2 description',
                     }

        resp = self.client.post(reverse('create_project:new'), form_data)
        self.assertEqual(resp.status_code, 200)


class ProjectApplicantTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.get(pk=2)
        self.project_position = ProjectPosition.objects.get(pk=1)
        self.project_applicant = ProjectApplicant.objects.create(user=self.user,
                                                                 position=self.project_position,
                                                                 status='p'
                                                                 )

    def test_applicant_status_update_view(self):
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
