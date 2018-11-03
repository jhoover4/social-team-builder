from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

avatar_storage = FileSystemStorage(location='/media/avatars')


class Profile(models.Model):
    """Extends the Django user model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    position = models.CharField(max_length=255)
    skills = models.ManyToManyField('Skills')
    avatar = models.ImageField(upload_to='avatars', default='blank-avatar.png')
    about_me = models.TextField()

    def __str__(self):
        return self.user.username


class Skills(models.Model):
    """Used to suggest skills for users and create new ones."""

    name = models.CharField(max_length=255)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
