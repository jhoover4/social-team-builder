from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from notifications.signals import notify

from team_builder import settings


class Project(models.Model):
    """Represents one project that a user owns."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = MarkdownxField(blank=True)
    time_involvement = models.IntegerField(default=60)
    applicant_requirements = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)

    @property
    def description_formatted_markdown(self):
        return markdownify(self.description)

    def __str__(self):
        return self.name


class ProjectPosition(models.Model):
    """Represents a position that a project needs."""

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = MarkdownxField(blank=True)
    related_skills = models.ManyToManyField('user_profile.Skill', blank=True)
    filled = models.BooleanField(default=False)
    time_involvement = models.IntegerField(default=60)  # eg: 10/hours a week. Done in minutes per week

    @property
    def description_formatted_markdown(self):
        return markdownify(self.description)

    def __str__(self):
        return self.name


class ProjectApplicant(models.Model):
    """Connects a user to the project they are applying for."""

    ACCEPTED = 'a'
    REJECTED = 'r'
    PENDING = 'p'
    STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    position = models.ForeignKey('ProjectPosition', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='p')
    time_on_project = models.IntegerField(default=0)

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        if instance.status == 'a':
            project_position = instance.position
            project_position.filled = True
            notify.send(instance, recipient=instance.user, verb="Congrats, you've been rejected for the {} position!".format(instance.position.name))
        elif instance.status == 'p':
            notify.send(instance, recipient=instance.user, verb='You applied to the {} position.'.format(instance.position.name))
        elif instance.status == 'r':
            notify.send(instance, recipient=instance.user, verb="Sorry, you've been rejected for the {} position.".format(instance.position.name))

    @staticmethod
    def pre_delete(sender, **kwargs):
        instance = kwargs.get('instance')
        notify.send(instance, recipient=instance.user,
                    verb="Your application for the {} position was removed.".format(instance.position.name))

    def __str__(self):
        return self.user.email + ":" + self.position.name


post_save.connect(ProjectApplicant.post_save, sender=ProjectApplicant)
pre_delete.connect(ProjectApplicant.pre_delete, sender=ProjectApplicant)
