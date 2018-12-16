from django.views.generic.detail import DetailView

from .models import Project


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
