# Generated by Django 2.2a1 on 2019-02-13 18:16

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('create_project', '0002_auto_20190209_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True),
        ),
        migrations.AlterField(
            model_name='projectposition',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True),
        ),
    ]