from django import forms
from . models import Course , CourseTopic , Personal , CourseStructure, ClassRoom
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CourseMarkContribution(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('midterm_exam','assginment','practice','project','final_exam')
        widgets = {
            'midterm_exam': forms.TextInput(attrs={'placeholder': 'Midterm Exam', 'style':'margin-bottom:2mm;border-radius:0%;'}),
            'assginment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Homework','style':'margin-bottom:2mm;border-radius:0%;'}),
            'practice': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Application','style':'margin-bottom:2mm;border-radius:0%;'}),
            'project': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Project','style':'margin-bottom:2mm;border-radius:0%;'}),
            'final_exam': forms.TextInput(attrs={'placeholder': 'Final Exam','style':'margin-bottom:2mm;border-radius:0%;'}),
        }


class TopicForm(forms.ModelForm):

    class Meta:
        model = CourseTopic
        fields = ['week_no','topic', 'document']
        



class PersonalForm(forms.ModelForm ):


    class Meta:
        model = Personal
        fields = ("user","faculty","department","identity_no","personal_no","first_name","last_name","phone","email")
        widgets = {
            'user': forms.TextInput(attrs={'type':'hidden'}),
        }


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields=('username',)

class PasswordForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields=('password1','password2')


class LessonForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('faculty', 'department', 'class_no', 'semester_no', 'course_code', 'course_name', 'lecturer', 'credit', 'course_language',
              'course_level',
              'aim_of_lesson',
              'course_content',
              'course_assistants',
              'course_document')
        
    # NOTE
    # 'course_resources',
    # 'course_topics',
    # 'course_structure', 'course_learning_outcomes'

class CourseStructureForm(forms.ModelForm):
    class Meta:
        model = CourseStructure
        fields=[
            'math_science',
            'engineering_science',
            'engineering_design',
            'liberal_arts',
            'educational_science',
            'science',
            'health_science',
            'area_information'
        ]


class ClassRoomForm(forms.ModelForm):

    class Meta:
        model = ClassRoom
        fields = ('room_no', 'day','lecture_time')