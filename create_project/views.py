from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Textarea
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from extra_views import InlineFormSetFactory

from .forms import ProjectForm, ProjectFormSet
from .models import Project, ProjectPosition


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


class ProjectPositionInline(InlineFormSetFactory):
    model = ProjectPosition
    fields = ['name', 'description', 'related_skills', 'filled', 'time_involvement']
    factory_kwargs = {'extra': 1,
                      'widgets': {
                          'description': Textarea(attrs={'cols': 40,
                                                         'rows': 10,
                                                         'placeholder': 'Position description...'}
                                                  )},
                      'labels': {
                          'filled': 'Filled?',
                      },
                      'help_texts': {'time_involvement': '(In minutes)'}
                      }


# class ProjectCreateView(LoginRequiredMixin, CreateWithInlinesView):
#     model = Project
#     inlines = [ProjectPositionInline]
#     fields = ['name', 'description', 'time_involvement', 'applicant_requirements']
#     template_name = 'project_create_edit.html'
#     login_url = '/profiles/login'
#
#     def forms_valid(self, form, inlines):
#         form.instance.owner = get_user(self.request)
#
#         return super(ProjectCreateView, self).forms_valid(form, inlines)
#         # return super().form_valid(form)
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()
#
#
# class ProjectUpdateView(LoginRequiredMixin, UpdateWithInlinesView):
#     model = Project
#     inlines = [ProjectPositionInline]
#     fields = ['name', 'description', 'time_involvement', 'applicant_requirements']
#     template_name = 'project_create_edit.html'
#     login_url = '/profiles/login'
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()

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

        if form.is_valid() and project_positions_form.is_valid():
            self.object = form.save(commit=False)
            form.instance.owner = get_user(self.request)
            form.save()

            project_positions_form.instance = self.object
            project_positions_form.save()

        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = '__all__'

    template_name = 'project_create_edit.html'


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('index')
