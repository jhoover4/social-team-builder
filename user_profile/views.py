from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from create_project.models import Project, ProjectApplicant, ProjectPosition
from .forms import SignUpForm, ProfileForm
from .models import CustomUser


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
            return HttpResponseRedirect(reverse('profiles:root', kwargs={'profile_id': user.pk}))
    return render(request, 'user_profile/signup.html', {'form': form})


@login_required
def profile_redirect(request):
    return HttpResponseRedirect(reverse('profiles:root', kwargs={'profile_id': request.user.id}))


@login_required
def edit_profile(request):
    bio_form = ProfileForm()
    if request.method == 'POST':
        bio_form = ProfileForm(data=request.POST)
        if bio_form.is_valid():
            bio_form.save()
            messages.success(
                request,
                "Profile updated."
            )
            return HttpResponseRedirect(reverse('profiles:profile', kwargs={'profile_id': request.user.id}))
    return HttpResponseRedirect(
        reverse('profiles:edit_profile', kwargs={'profile_id': request.user.id, 'bio_form': bio_form}))


def view_profile(request, profile_id):
    """View a single user profile."""

    user = CustomUser.objects.get(id=profile_id)

    return render(request, 'user_profile/profile.html', {
        'user': user,
    })


def view_dashboard(request, profile_id):
    """User dashboard includes user created projects and submitted applications.
    Can filter based on application status, project name, and project needs.
    """

    user = CustomUser.objects.get(id=profile_id)

    status_query = request.GET.get('status', None)
    project_query = request.GET.get('project', None)
    job_query = request.GET.get('job', None)

    query = Q()
    if status_query:
        query &= Q(status=status_query)
    if project_query:
        query &= Q(position__project__name__iexact=project_query)
    if job_query:
        query &= Q(position__name__iexact=job_query)

    if query:
        applications = ProjectApplicant.objects.filter(query).distinct()
    else:
        applications = ProjectApplicant.objects.all()

    projects = Project.objects.all().values('pk','name')
    positions = ProjectPosition.objects.filter(pk__in=[project['pk'] for project in projects]).values('name')

    return render(request, 'user_profile/application_dashboard.html', {
        'user': user,
        'projects': projects,
        'positions': positions,
        'applications': applications,
        'searched_status': status_query,
        'searched_project': project_query,
        'searched_job': job_query
    })
