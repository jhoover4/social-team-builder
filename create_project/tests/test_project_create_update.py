from django.test import TestCase
from django.urls import reverse

from create_project.forms import ProjectForm, ProjectFormSet
from create_project.models import Project
from user_profile.models import CustomUser
from user_profile.models import Skill


class ProjectUpdateCreateTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=1)
        self.test_project = Project.objects.get(pk=1)
        self.skill = Skill.objects.get(pk=1)

        self.client.login(email=self.test_user.email, password='&Oa0sMqvXJT0')

    def test_create_project_view(self):
        """
        Should be able to see a valid view for creating a project.
        """

        resp = self.client.get(reverse('create_project:new'))

        self.assertTemplateUsed(resp, 'project_create_edit.html')
        self.assertEqual(resp.status_code, 200)

    def test_edit_project_view(self):
        """
        Should be able to see a valid view for editing a project.
        """

        resp = self.client.get(reverse('create_project:edit', kwargs={'pk': self.test_project.pk}))

        self.assertTemplateUsed(resp, 'project_create_edit.html')
        self.assertEqual(resp.status_code, 200)

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
