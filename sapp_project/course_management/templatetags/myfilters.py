from django import template
import os
from ..models import Course
import datetime
register = template.Library()



def basename(value):
    return os.path.basename(value)

def student_score(student, course_no):
    return student.student_mark.filter(course = Course.objects.get(pk=int(course_no))).first()

@register.filter
def str_to_time(value):
    return datetime.datetime.strptime(value, '%I:%M%p').time()

@register.filter
def get_mark(course, student):
    return course.student_mark.all().filter(student=student).first()


register.filter('basename', basename)
register.filter('student_score', student_score)