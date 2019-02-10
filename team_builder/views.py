from django.shortcuts import render

from create_project.models import Project, ProjectPosition


def index(request):
    """
    Index view is used for showing and filtering minerals. Search box takes precedence over letter filtering.
    """

    position_query = request.GET.get('position', None)
    if position_query:
        projects = Project.objects.filter(projectposition__name__iexact=position_query)
    else:
        projects = Project.objects.all()

    positions = ProjectPosition.objects.filter(project__pk__in=[project.pk for project in projects]).values('name')

    return render(request, 'index.html', {
        'available_projects': projects,
        'available_positions': positions,
        'searched_position': position_query,
    })
