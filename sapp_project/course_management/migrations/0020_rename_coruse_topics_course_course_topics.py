# Generated by Django 4.2 on 2023-04-22 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0019_alter_course_coruse_topics'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='coruse_topics',
            new_name='course_topics',
        ),
    ]
