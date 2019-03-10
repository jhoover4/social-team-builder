from django.test import TestCase

from user_profile.models import CustomUser, Skill


class UserModelTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=1)

    def test_custom_user_repr(self):
        assert self.test_user.email == str(self.test_user)

    def test_create_user_permissions(self):
        """Regular user should be created with no staff permissions."""

        user = CustomUser.objects.create_user('test@test.com', 'foo')

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_permissions(self):
        """Regular user should be created with no staff permissions."""

        user = CustomUser.objects.create_superuser('test@test.com', 'foo')

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_base_user_no_email(self):
        """Should raise a value error if no email is provided."""

        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='foo')


class ProfileModelTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=1)

    def test_profile_repr(self):
        assert self.test_user.email == str(self.test_user.profile)

    def test_profile_about_me_markdown(self):
        """Should return formatted string in markdown."""

        self.test_user.profile.about_me = "# Some markdown"

        self.assertEqual(self.test_user.profile.about_me_formatted_markdown, "<h1>Some markdown</h1>")


class SkillModelTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.skill = Skill.objects.get(pk=1)

    def test_skill_repr(self):
        assert self.skill.name == str(self.skill)
