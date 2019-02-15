from django import template
from create_project.models import ProjectApplicant
from django import forms

register = template.Library()


@register.simple_tag(name='url_add_replace_attr')
def url_add_replace_attr(request, field, value):
    url_string = request.GET.copy()

    url_string.__setitem__(field, value)

    return u"?%s" % (url_string.urlencode())


@register.simple_tag(name='url_del_attr')
def url_del_attr(request, field):
    url_string = request.GET.copy()

    if url_string.__contains__(field):
        url_string.__delitem__(field)

    return u"?%s" % (url_string.urlencode())


@register.inclusion_tag('markdown_information.html')
def markdown_information():
    return


@register.inclusion_tag('applicant_status_select.html')
def applicant_status_select(current_status, applicant_pk):
    choices = ProjectApplicant.STATUS_CHOICES

    widget = forms.Select(choices=choices)
    widget_html = widget.render('applicant-status-widget', 'applicant-status-widget',
                                attrs={'data-id': applicant_pk, 'data-status': current_status, 'selected': False})

    return {'current_status': current_status,
            'widget': widget_html
            }
