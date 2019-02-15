from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProjectForm, ProjectFormSet
from .models import Project, ProjectApplicant


class ProjectDetailView(DetailView):
    model = Project

    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_time_involvement_hours = round(context['project'].time_involvement / 60, 1)

        if float(project_time_involvement_hours).is_integer():
            context['project'].time_involvement_hours = int(project_time_involvement_hours)
        else:
            context['project'].time_involvement_hours = project_time_involvement_hours

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'project_create_edit.html'
    form_class = ProjectForm
    login_url = '/profiles/login'

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

            if project_positions_form.is_valid():
                formset = project_positions_form.save(commit=False)
                for position_form in formset:
                    position_form.project = self.object
                    position_form.save()
                project_positions_form.save()
                project_positions_form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project_create_edit.html'
    form_class = ProjectForm
    login_url = '/profiles/login'

    def get_success_url(self):
        return reverse_lazy('create_project:root', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['project_positions_formset'] = ProjectFormSet(self.request.POST, instance=self.object)
        else:
            context['project_positions_formset'] = ProjectFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        project_positions_form = context['project_positions_formset']

        if form.is_valid():
            form.save(commit=False)
            form.instance.owner = self.request.user
            self.object = form.save()

            if project_positions_form.is_valid():
                formset = project_positions_form.save(commit=False)
                for position_form in formset:
                    position_form.project = self.object
                    position_form.save()
                project_positions_form.save()
                project_positions_form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('index')


class ApplicantStatusUpdateView(UpdateView):
    """This view will only work with AJAX requests."""

    model = ProjectApplicant
    fields = ['status']
    http_method_names = ['post']
    success_url = '/'

    def render_to_response(self, context, **response_kwargs):
        """Allow AJAX requests to be handled more gracefully """

        if self.request.is_ajax():
            return JsonResponse('Success', safe=False, **response_kwargs)
        else:
            return JsonResponse('Request must be valid JSON.', status=400)
