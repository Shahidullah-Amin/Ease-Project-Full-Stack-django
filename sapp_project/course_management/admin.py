from django.contrib import admin
from .models import (Personal, Student, Faculty, Department, Course,
                     Mark, CourseStructure, CourseTopic, CourseOutcomes, Resource , ClassRoom)


admin.site.register(Personal)
admin.site.register(Mark)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(CourseOutcomes)
admin.site.register(CourseStructure)
admin.site.register(CourseTopic)
admin.site.register(Resource)
admin.site.register(ClassRoom)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = (('faculty', 'department', 'class_no', 'semester','semester_no'), 'course_code', 'course_name', 'lecturer', 'credit', 'course_language',
              'course_level',
              'aim_of_lesson',
              'course_content',
              'course_assistants',
              'course_resources',
              'course_topics',
              'course_structure', 'course_learning_outcomes', ('midterm_exam', 'final_exam', 'assginment', 'practice', 'project'),'course_document')
