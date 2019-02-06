from django.forms import ModelForm, Textarea
from django.forms.models import inlineformset_factory

from .models import Project, ProjectPosition


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'time_involvement', 'applicant_requirements')


ProjectFormSet = inlineformset_factory(Project,
                                       ProjectPosition,
                                       extra=1,
                                       fields='__all__',
                                       widgets={
                                           'description': Textarea(attrs={'cols': 40,
                                                                          'rows': 10,
                                                                          'placeholder': 'Position description...'}
                                                                   )},
                                       labels={
                                           'filled': 'Filled?',
                                       },
                                       help_texts={
                                           'time_involvement': 'In minutes',
                                       }
                                       )
