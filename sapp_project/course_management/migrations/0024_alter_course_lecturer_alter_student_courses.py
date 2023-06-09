# Generated by Django 4.2 on 2023-05-13 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0023_rename__class_student_class_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lecturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_set', to='course_management.personal'),
        ),
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(related_name='student_set', to='course_management.course'),
        ),
    ]
