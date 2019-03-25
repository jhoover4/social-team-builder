from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from create_project.models import Project, ProjectApplicant, ProjectPosition
from .forms import SignUpForm, ProfileForm, CustomUserChangeForm
from .models import CustomUser, Skill


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


def get_all_user_position_applicants(profile):
    try:
        all_positions = ProjectApplicant.objects.select_related('position').filter(
            Q(user=profile)).annotate(status_display=F('status'))
    except ProjectApplicant.DoesNotExist:
        all_positions = None

    return all_positions


@login_required
def edit_profile(request):
    user = request.user
    SkillFormSet = modelformset_factory(Skill, fields=('name',), can_delete=True)

    all_positions = get_all_user_position_applicants(user)

    if all_positions:
        current_positions = all_positions.filter(Q(status='a')).values(
            'position__project__name')
        applications = all_positions.exclude(status='a').values(
            'position__project__pk', 'position__project__name'
        )
    else:
        current_positions = None
        applications = None

    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=user)
        bio_form = ProfileForm(data=request.POST, instance=user.profile)
        skill_formset = SkillFormSet(data=request.POST, queryset=Skill.objects.filter(profile=user.profile))

        bio_form.user = user

        if form.is_valid() and bio_form.is_valid():
            form.save()
            bio_form.save(commit=False)
            bio_form.instance.user = user

            if skill_formset.is_valid():
                formset = skill_formset.save(commit=False)
                for skill_form in formset:
                    skill_form.save()
                    bio_form.instance.skills.add(skill_form)
                skill_formset.save()
            bio_form.save()
            messages.success(
                request,
                "Profile updated."
            )
            return HttpResponseRedirect(reverse('profiles:root', kwargs={'profile_id': user.id}))

    else:
        form = CustomUserChangeForm(instance=user)
        bio_form = ProfileForm(instance=user.profile)
        skill_formset = SkillFormSet(queryset=Skill.objects.filter(profile=user.profile))

    return render(request, 'user_profile/profile_edit.html',
                  {'form': form,
                   'bio_form': bio_form,
                   'skill_formset': skill_formset,
                   'applications': applications,
                   'current_positions': current_positions}
                  )


def view_profile(request, profile_id):
    """
    View a single user profile. If the viewer is not the profile's owner,
    then give them application approval functionality.
    If the viewer is the profile owner, they can edit their profile.
    """

    current_profile = CustomUser.objects.get(id=profile_id)
    all_positions = get_all_user_position_applicants(current_profile)

    if all_positions:
        current_positions = all_positions.filter(Q(status='a')).values(
            'position__project__pk', 'position__project__name')
        applications = all_positions.exclude(status='a')
    else:
        current_positions = None
        applications = None

    return render(request, 'user_profile/profile.html', {
        'current_profile': current_profile,
        'current_positions': current_positions,
        'applications': applications,
    })


def view_dashboard(request, profile_id):
    """
    User dashboard includes user created projects and submitted applications.
    Can filter based on application status, project name, and project needs.
    """

    user = CustomUser.objects.get(id=profile_id)

    status_query = request.GET.get('status', None)
    project_query = request.GET.get('project', None)
    job_query = request.GET.get('job', None)

    query = Q(position__project__owner=user)
    if status_query:
        query &= Q(status=status_query)
    if project_query:
        query &= Q(position__project__name__iexact=project_query)
    if job_query:
        query &= Q(position__name__iexact=job_query)

    applications = ProjectApplicant.objects.filter(query).distinct()

    projects = Project.objects.filter(owner=user).values('pk', 'name')
    positions = ProjectPosition.objects.filter(project__pk__in=[project['pk'] for project in projects]).values('name')

    return render(request, 'user_profile/application_dashboard.html', {
        'user': user,
        'projects': projects,
        'positions': positions,
        'applications': applications,
        'searched_status': status_query,
        'searched_project': project_query,
        'searched_job': job_query
    })
