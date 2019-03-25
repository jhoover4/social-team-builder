from django.test import TestCase

from create_project.models import Project, ProjectPosition, ProjectApplicant
from user_profile.models import CustomUser


class UserModelTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=2)
        self.project_position = ProjectPosition.objects.get(pk=1)
        self.project_applicant = ProjectApplicant.objects.create(user=self.test_user,
                                                                 position=self.project_position,
                                                                 status='p'
                                                                 )

    def test_project_repr(self):
        project = Project.objects.get(pk=1)
        assert project.name == str(project)

    def test_project_position_repr(self):
        assert self.project_position.name == str(self.project_position)

    def test_project_applicant_repr(self):
        assert self.test_user.email + ':' + self.project_position.name == str(self.project_applicant)
