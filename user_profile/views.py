from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import SignUpForm


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            username = request.user.email
            return HttpResponseRedirect(reverse('profiles:root', kwargs={'profile_id': username}))
    return render(request, 'user_profile/signup.html', {'form': form})


@login_required
def profile_redirect(request):
    return HttpResponseRedirect(reverse('profiles:root', kwargs={'profile_id': request.user.id}))
