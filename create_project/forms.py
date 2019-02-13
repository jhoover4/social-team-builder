from django.forms import ModelForm, Textarea, TextInput
from django.forms.models import inlineformset_factory

from .models import Project, ProjectPosition


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'time_involvement', 'applicant_requirements')
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Project Title', 'class': 'circle--input--h1'}),
            'description': Textarea(attrs={'placeholder': 'Position description...'}),
            'time_involvement': Textarea(attrs={'placeholder': 'Time estimate', 'class': 'circle--textarea--input'}),
        }


ProjectFormSet = inlineformset_factory(Project,
                                       ProjectPosition,
                                       form=ProjectForm,
                                       extra=1,
                                       max_num=1,
                                       fields=('project', 'name', 'description', 'related_skills', 'time_involvement'),
                                       widgets={
                                           'name': TextInput(attrs={'placeholder': 'Position Title',
                                                                    'class': 'circle--input--h3'}
                                                             ),
                                           'description': Textarea(attrs={'cols': 40,
                                                                          'rows': 10,
                                                                          'placeholder': 'Position description...'}
                                                                   ),
                                       },
                                       help_texts={
                                           'time_involvement': 'In minutes',
                                       }
                                       )
