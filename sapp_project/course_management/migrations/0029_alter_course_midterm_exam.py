# Generated by Django 4.2 on 2023-05-17 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0028_alter_course_assginment_alter_course_final_exam_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='midterm_exam',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
