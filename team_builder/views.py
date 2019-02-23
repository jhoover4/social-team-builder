from django.db.models import Q
from django.shortcuts import render

from create_project.models import Project, ProjectPosition


def index(request):
    """
    Index view is used for showing and filtering projects with open positions.
    Projects can be searched in search box or by position.
    """
    
    search_query = request.GET.get('q', None)
    position_query = request.GET.get('position', None)

    if search_query:
        projects = Project.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    elif position_query:
        projects = Project.objects.filter(projectposition__name__iexact=position_query)
    else:
        projects = Project.objects.all()

    positions = ProjectPosition.objects.filter().values('name')

    return render(request, 'index.html', {
        'available_projects': projects,
        'available_positions': positions,
        'searched_position': position_query,
    })
