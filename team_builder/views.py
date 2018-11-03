from django.shortcuts import render


def index(request):
    """
    Index view is used for showing and filtering minerals. Search box takes precedence over letter filtering.
    """

    return render(request, 'index.html')
