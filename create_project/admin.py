from django.contrib import admin

from .models import Project, ProjectApplicant, ProjectPosition


class ProjectPositionInline(admin.TabularInline):
    model = ProjectPosition


class ProjectApplicantInline(admin.TabularInline):
    model = ProjectApplicant


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectApplicantInline,
        ProjectPositionInline,
    ]


admin.site.register(Project, ProjectAdmin)
