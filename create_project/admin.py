from django.contrib import admin

from .models import Project, ProjectPosition, ProjectApplicant


class ProjectPositionInline(admin.TabularInline):
    model = ProjectPosition


class ProjectApplicantInline(admin.TabularInline):
    model = ProjectApplicant


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectPositionInline,
    ]


class ProjectPositionAdmin(admin.ModelAdmin):
    inlines = [
        ProjectApplicantInline,
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectPosition, ProjectPositionAdmin)
