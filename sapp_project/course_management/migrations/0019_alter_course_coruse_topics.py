# Generated by Django 4.2 on 2023-04-22 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0018_coursetopic_delete_coursetopics_course_coruse_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='coruse_topics',
            field=models.ManyToManyField(blank=True, null=True, to='course_management.coursetopic'),
        ),
    ]