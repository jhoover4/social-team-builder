import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProjectForm, ProjectFormSet
from .models import Project, ProjectPosition, ProjectApplicant


class ProjectDetailView(DetailView):
    model = Project

    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            try:
                user_applied_projects = ProjectApplicant.objects.filter(position=OuterRef('pk'), user=user)
                project_positions = ProjectPosition.objects.filter(project__id=self.object.id).annotate(
                    user_applied=Subquery(user_applied_projects.values('id'))).order_by('pk')
            except ProjectApplicant.DoesNotExist:
                project_positions = None
        else:
            project_positions = ProjectPosition.objects.filter(project__id=self.object.id).order_by('pk')

        context['project_positions'] = project_positions
        context['is_project_owner'] = self.object.owner == user

        project_time_involvement_hours = round(context['project'].time_involvement / 60, 1)
        if float(project_time_involvement_hours).is_integer():
            context['project'].time_involvement_hours = int(project_time_involvement_hours)
        else:
            context['project'].time_involvement_hours = project_time_involvement_hours

        return context


class ProjectPositionInlineFormsetMixin:
    """Mixin to overwrite CBVs for project position inline formset use."""

    def get_success_url(self):
        return reverse_lazy('create_project:root', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['project_positions_formset'] = ProjectFormSet(self.request.POST)
        else:
            context['project_positions_formset'] = ProjectFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        project_positions_form = context['project_positions_formset']

        if form.is_valid():
            form.save(commit=False)
            form.instance.owner = self.request.user
            self.object = form.save()
            self.object.save()

            project_positions_form.instance = self.object
            if project_positions_form.is_valid():
                project_positions_form.save()
            else:
                for position_form in project_positions_form:
                    if position_form.is_valid():
                        position_form.save()

        return HttpResponseRedirect(self.get_success_url())


class ProjectCreateView(LoginRequiredMixin, ProjectPositionInlineFormsetMixin, CreateView):
    model = Project
    template_name = 'project_create_edit.html'
    form_class = ProjectForm
    login_url = '/profiles/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['project_positions_formset'] = ProjectFormSet(self.request.POST)
        else:
            context['project_positions_formset'] = ProjectFormSet()
        return context


class ProjectUpdateView(LoginRequiredMixin, ProjectPositionInlineFormsetMixin, UpdateView):
    model = Project
    template_name = 'project_create_edit.html'
    form_class = ProjectForm
    login_url = '/profiles/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['project_positions_formset'] = ProjectFormSet(self.request.POST, instance=self.object)
        else:
            context['project_positions_formset'] = ProjectFormSet(instance=self.object)
        return context


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('index')


class AjaxResponseMixin:
    """Mixin to overwrite CBVs for Ajax-only requesting."""

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return JsonResponse('Request must be AJAX.', safe=False, status=400)

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            data = {
                'pk': self.object.pk,
            }
            return HttpResponse(json.dumps(data), status=200, content_type='application/json')
        else:
            return JsonResponse('Request must be AJAX.', safe=False, status=400)


class ApplicantCreateView(LoginRequiredMixin, AjaxResponseMixin, CreateView):
    """This view will only work with AJAX requests."""

    model = ProjectApplicant
    fields = ['user', 'position']
    http_method_names = ['post']


class ApplicantDeleteView(LoginRequiredMixin, AjaxResponseMixin, DeleteView):
    """This view will only work with AJAX requests."""

    model = ProjectApplicant

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponse(status=204, content_type='application/json')


class ApplicantStatusUpdateView(LoginRequiredMixin, AjaxResponseMixin, UpdateView):
    """This view will only work with AJAX requests."""

    model = ProjectApplicant
    fields = ['status']
    http_method_names = ['post']
