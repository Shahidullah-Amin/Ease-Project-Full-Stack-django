# Generated by Django 4.2 on 2023-04-19 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0010_alter_course_course_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='_class',
            new_name='class_no',
        ),
    ]
