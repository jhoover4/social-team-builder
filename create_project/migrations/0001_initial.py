# Generated by Django 2.1.2 on 2019-02-09 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('time_involvement', models.IntegerField(default=60)),
                ('applicant_requirements', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectApplicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('a', 'Accepted'), ('r', 'Rejected'), ('p', 'Pending')], max_length=10, null=True)),
                ('time_on_project', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('filled', models.BooleanField(default=False)),
                ('time_involvement', models.IntegerField(default=60)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_project.Project')),
                ('related_skills', models.ManyToManyField(to='user_profile.Skill')),
            ],
        ),
        migrations.AddField(
            model_name='projectapplicant',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_project.ProjectPosition'),
        ),
        migrations.AddField(
            model_name='projectapplicant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
