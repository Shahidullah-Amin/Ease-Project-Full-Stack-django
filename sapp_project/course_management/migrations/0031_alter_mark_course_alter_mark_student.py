# Generated by Django 4.2 on 2023-05-19 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0030_alter_mark_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_mark', to='course_management.course'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_mark', to='course_management.student'),
        ),
    ]
