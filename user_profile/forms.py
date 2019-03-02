from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import Textarea, TextInput

from .models import CustomUser, Profile, Skill


class SignUpForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('position', 'about_me')
        # fields = ('position', 'avatar', 'about_me')

        widgets = {
            'position': TextInput(attrs={'placeholder': 'Position', 'class': 'circle--input--h2'}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'First Name', 'class': 'circle--input--h1'}),
            'last_name': TextInput(attrs={'placeholder': 'Last Name', 'class': 'circle--input--h1'}),
        }
