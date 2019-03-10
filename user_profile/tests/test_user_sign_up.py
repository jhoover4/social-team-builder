from django.test import TestCase
from django.urls import reverse

from user_profile.forms import SignUpForm
from user_profile.models import CustomUser, Skill


class UserSignUpTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.test_user = CustomUser.objects.get(pk=1)
        self.skill = Skill.objects.get(pk=1)

        self.client.login(email=self.test_user.email, password='&Oa0sMqvXJT0')

    def test_view_get(self):
        """Should be able to see a valid view for creating a project."""

        resp = self.client.get(reverse('user_profile:sign_up'))

        self.assertTemplateUsed(resp, 'user_profile/signup.html')
        self.assertEqual(resp.status_code, 200)

    def test_create_user(self):
        """Should be able to see a valid view for creating a project."""

        form_data = {'email': 'bob@test.com',
                     'password1': 'test',
                     'password2': 'test'
                     }

        resp = self.client.post(reverse('user_profile:sign_up'), form_data)
        self.assertEqual(resp.status_code, 302)

        new_user = CustomUser.objects.latest('pk')
        self.assertEqual('bob@test.com', new_user.email)

    def test_form(self):
        """Should be able to use a valid email and password to submit data to sign up a new user."""

        form_data = {'email': 'bob@test.com',
                     'password1': 'test',
                     'password2': 'test'
                     }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_password_mismatch(self):
        """Form should throw error if passwords don't match."""

        form_data = {'email': 'bob@test.com',
                     'password1': 'test',
                     'password2': 'asdfd'
                     }
        form = SignUpForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'][0], "Passwords don't match")
