from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from . models import Course, CourseTopic, Mark, ClassRoom, Personal , Faculty , Department , Student , ClassRoom
from . forms import CourseMarkContribution, TopicForm, PersonalForm, UserForm, PasswordForm , LessonForm, CourseStructureForm , ClassRoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import reverse
import os

from django.contrib.auth import authenticate , login 


@login_required
def edit_class(request , id):
    id = int(id)
    if ClassRoom.objects.filter(id=id).exists():
        class_room = ClassRoom.objects.get(pk=id)

        form = ClassRoomForm(instance=class_room)

        if request.method=='POST':
            form = ClassRoomForm(request.POST, instance=class_room)

            if form.is_valid():
                form.save()
                messages.success(request , 'Class has been updated successfully')
                return redirect(reverse('all-classes'))

        return render(request , 'course_management/administration/edit_class.html', {'form':form})

       
    return HttpResponse('<h1><center>Something went wrong!</center></h1>')


@login_required
def delete_class(request , id):
    id = int(id)
    if ClassRoom.objects.filter(id=id).exists():
        class_room = ClassRoom.objects.get(pk=id)

        class_room.delete()
        messages.success(request, f'{class_room} has been deleted successfully')
        return redirect('all-classes')
    return HttpResponse('<h1><center>Something went wrong!</center></h1>')


@login_required
def add_class(request):

    courses = None
    selected_class = request.POST.get('class-select')
    if selected_class:
        selected_class = int(selected_class)
        courses = Course.objects.all().filter(class_no=selected_class)

    form = ClassRoomForm()

    class_options = [
        'Software Engineering I',
        'Software Engineering II',
        'Software Engineering III',
        'Software Engineering IV',
    ]

    course_id = request.POST.get('course')
    
    if request.method=='POST' and request.POST.get('course'):
        form=ClassRoomForm(request.POST)
        if form.is_valid():
            cls_room = form.save()
            cls_room.course = Course.objects.get(pk=int(course_id))
            cls_room.save()
            messages.success(request , 'Class has been added successfully')
            return redirect(reverse('all-classes'))
        

    return render(request, 'course_management/administration/add_class.html', {'form':form , 'courses':courses , 'selected_class':selected_class,'class_options':class_options})



@login_required
def get_classes(request):

    class_rooms = ClassRoom.objects.all()

    return render(request , 'course_management/administration/all_classes.html' , {'class_rooms':class_rooms})


@login_required
def delete_lesson(request , id):
    id = int(id)
    if request.META.get('HTTP_REFERER') == request.build_absolute_uri(reverse('lessons')):

        if Course.objects.filter(id=id).exists():
            course = Course.objects.get(pk=id)
            course_name = course.course_name
            course.delete()
            messages.success(request ,f"'{course_name}' has been deleted successfully")
            return redirect(reverse('lessons'))
        
        return HttpResponse('<center><h1>Something went wrong!</h1></center>')
    return redirect(reverse('notfound'))





@login_required
def edit_lesson(request , id):
    id = int(id)

    if Course.objects.filter(id=id).exists():

        course = Course.objects.get(pk=id)
        course_name = course.course_name
        
        form  = LessonForm(instance=course)
        strcuture_form = CourseStructureForm(instance=course.course_structure)

        if request.method=='POST':
            form  = LessonForm( request.POST,request.FILES,instance=course)
            strcuture_form = CourseStructureForm(request.POST,instance=course.course_structure)
            if form.is_valid() and strcuture_form.is_valid():
                form.save()
                strcuture_form.save()
                messages.success(request, f"'{course_name}' edited successfully")
                return redirect(reverse('lessons'))


        return render(request , 'course_management/administration/edit_lesson.html'  , {'form':form , 'structure_form':strcuture_form})

    
    return HttpResponse('<center><h1>Something went wrong!</h1></center>')



@login_required
def add_lesson(request):

    form  = LessonForm()
    strcuture_form = CourseStructureForm()

    if(request.method=="POST"):
        form=LessonForm( request.POST , request.FILES)
        strcuture_form = CourseStructureForm(request.POST)
        if form.is_valid() and strcuture_form.is_valid():
            structure = form.save()
            structure.course_structure = strcuture_form.save()
            structure.save()
            messages.success(request,'Lesson has been added successfully')
            return redirect('lessons')


    return render(request , 'course_management/administration/add_lesson.html'  , {'form':form , 'structure_form':strcuture_form})





@login_required
def get_all_lessons(request):

    courses = Course.objects.all()

    return render(request , 'course_management/administration/lessons.html', {'courses':courses})





@login_required
def edit_teacher(request, id):


    if(Personal.objects.filter(id=int(id)).exists()):

        teacher = Personal.objects.get(pk=int(id))

        form = PersonalForm(instance=teacher)
        user_form = UserForm(instance=teacher.user)

        if(request.method=='POST'):

            username=request.POST.get('username')

            form = PersonalForm(request.POST ,instance=teacher)
            user_form = UserForm(request.POST , instance=teacher.user)
            
            if user_form.is_valid() and  form.is_valid():
                user = teacher.user
                user.username = username
                user.save()

                teacher.faculty = Faculty.objects.get( pk=int(request.POST.get('faculty')))
                teacher.department = Department.objects.get( pk=int(request.POST.get('department')))
                teacher.identity_no = request.POST.get('identity_no')
                teacher.personal_no = request.POST.get('personal_no')
                teacher.first_name = request.POST.get('first_name')
                teacher.last_name = request.POST.get('last_name')
                teacher.phone = request.POST.get('phone')
                teacher.email = request.POST.get('email')
                teacher.save()
                messages.success( request,'Teacher has been updated successfully')
                return redirect(reverse('teachers'))
                
            else:
                form=PersonalForm(request.POST , instance=teacher)
                if form.is_valid:
                    print('success')

        return render(request , 'course_management/administration/edit_teacher.html', {'form':form , 'user_form':user_form})


    return redirect('teachers')


@login_required
def delete_confirmation(request , id):
    teacher = User.objects.get(pk=int(id)).personal
    return render(request, 'course_management/administration/delete_confirmation.html', {'id':id,'teacher':teacher})


@login_required
def delete_teacher(request , id):

    if request.META.get('HTTP_REFERER') == request.build_absolute_uri(reverse('teachers')) or request.META.get('HTTP_REFERER')==request.build_absolute_uri(reverse('delete-confirm', kwargs={'id':id})):
        if User.objects.filter(id=int(id)).exists():
            user = User.objects.get(pk=int(id))
            username = user.username
            user.delete()
            messages.success( request,f"'{username}' has been deleted successfully")
            return redirect(reverse('teachers'))
        else:
            return redirect('notfound')


    else:
        return redirect('notfound')


@login_required
def notfound(request):

    return render(request , 'course_management/administration/not_found_page.html')



@login_required
def add_teacher(request):

    form = PersonalForm()
    user_form = UserForm()
    password_form = PasswordForm()


    if(request.method=='POST'):
        username=request.POST.get('username')
        password1=request.POST.get('password1')

        user_form = UserForm(request.POST)
        password_form = PasswordForm(request.POST)
        
        if user_form.is_valid() and password_form.is_valid():
            user = User.objects.create(username=username , password=password1)
            user.save()
            copy_post = request.POST.copy()


            copy_post = request.POST.copy()
            copy_post['user']=user.pk
            form = PersonalForm(copy_post)

            if form.is_valid():
                form.save()
                messages.success(request, "Teacher has been added successfully")
                return redirect('teachers')
            else:
                user.delete()
        else:
            form=PersonalForm(request.POST)
            if form.is_valid:
                pass



    return render(request ,'course_management/administration/add_teacher.html' , {'password_form':password_form,'form':form, 'user_form':user_form })


@login_required
def get_all_teachers(request):

    teachers = Personal.objects.all()

    return render(request , 'course_management/administration/teachers.html', {'teachers':teachers})




@login_required
def evaluate_student(request, id=None):
    
    if hasattr(request.user , 'personal'):

        selected_id = request.POST.get('selected_course_students') 
        students = None
        course= None
        student_ordered_marks=None
        query = None

        

        if selected_id:
            return redirect(reverse('evaluate-student-score', kwargs={'id':selected_id}))


        if id:
            selected_id = int(id)
            course = Course.objects.get(pk=selected_id)
            students = course.student_set.all()
            student_ordered_marks= Mark.objects.all().filter(course=course).order_by('-marks')

            if request.POST.get('student_search_bar'):

                query = request.POST.get('student_search_bar')
                students = course.student_set.all().filter(Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_no__icontains=query))
        
        if request.method=='POST':
            if request.POST.get('student-score-form'):
                success = False
                for student in students:
                    if student.student_mark.all().filter(course=course).first():
                        mark_model = student.student_mark.all().filter(course=course).first()
                        marks = request.POST.get(student.student_no)
                        if marks:
                            mark_model.marks=int(marks)
                            mark_model.save()
                        print(mark_model)
                    else:
                        mark = Mark.objects.create(student = student , course = course , marks= request.POST.get(student.student_no) )
                        mark.save()
                    success = True
                if success:
                    messages.success(request , 'Score has been evaluated successfully')

        return render(request , 'course_management/evaluate_student_score.html', {'student_ordered_marks':student_ordered_marks, 'searched':query,'course':course,'students':students , 'selected_id':selected_id})

    return HttpResponse('<h1>404</h1>')



@login_required
def remove_topic(request,  id):
    
    couser_id = os.path.basename(request.META.get('HTTP_REFERER'))

    topic = CourseTopic.objects.filter(id=id).first()

    if topic:
        if topic.document:
            os.remove(topic.document.path)
        topic.delete()
        return redirect(reverse('add-topic', kwargs={"id":couser_id}))
    messages.error(request, 'Somthing went wrong!')
    return redirect(reverse('add-topic', kwargs={"id":couser_id}))



@login_required
def add_topic(request , id=None):
    if(hasattr(request.user , 'personal')):
        course_user = request.user.personal
    else:
        course_user = request.user.student 
    


    form = TopicForm()

    selected_id = request.POST.get('selected_course_add_topic')


    course = None
    course_topics = None
    if selected_id is not None:
        return redirect(reverse('add-topic', kwargs={'id':selected_id}))

    if id is not None:
        selected_id = int(id)
        course = Course.objects.get(pk = selected_id)
        course_topics = course.course_topics.all()

    

    if(request.method == 'POST'):
        form = TopicForm(request.POST)
        
        if form.is_valid():

            if course.course_topics.filter(week_no=int(request.POST.get('week_no'))).exists():
                form.add_error('week_no' , "Topic with Week No "+request.POST.get('week_no')+" already exists.")
                return render(request  , 'course_management/add_topic.html' , {'course_user':course_user,'form':form ,'course':course, 'course_topics':course_topics ,'selected_id':selected_id})

            messages.success(request , 'Topic has been added successfully')
            
            

            topic = CourseTopic(week_no=request.POST.get('week_no'), topic = request.POST.get('topic') , document=request.FILES.get('document'))
            topic.save()
            course.course_topics.add(topic)
            return redirect(reverse('add-topic', kwargs={'id':id}))

    return render(request  , 'course_management/add_topic.html' , {'course_user':course_user,'form':form ,'course':course, 'course_topics':course_topics ,'selected_id':selected_id})





@login_required
def evaluate_course(request):
    if(hasattr(request.user , 'personal')):
        course_user = request.user.personal
    else:
        course_user = request.user.student 
    
    selected_course_id = request.POST.get('course_select_mark')


    print(request.build_absolute_uri(reverse('courses')))

    if selected_course_id != None:
        return redirect('/mark-contribution/'+str(selected_course_id))


    
    form = CourseMarkContribution()

        
    return render(request , 'course_management/evaluate_lessons.html', { 'course_user':course_user , 'form':form ,'selected_course_id':selected_course_id })



@login_required
def mark_cotribution(request , id):

    if Course.objects.filter(id=int(id)).exists():
        if(hasattr(request.user , 'personal')):
           course_user = request.user.personal
        else:
            course_user = request.user.student 
        
        selected_course_id = request.POST.get('course_select_mark')

        if selected_course_id != None:
            selected_course_id  = int(selected_course_id)
            course = Course.objects.get(pk=selected_course_id)
            form = CourseMarkContribution(instance=course)
        else:
            selected_course_id = int(id)
            course = Course.objects.get(pk = selected_course_id )
            form = CourseMarkContribution(instance=course)

        if request.method == 'POST':
            if request.POST.get('midterm_exam'):
                form = CourseMarkContribution(request.POST , instance=course)
                if form.is_valid():
                    form.save()
                    messages.success(request , 'Course has been edited successfully', 'success')
                    return redirect(reverse('course-info', kwargs={'id':selected_course_id}))


        
        return render(request , 'course_management/evaluate_lessons.html' , {'form':form , 'course_info':course , 'selected_course_id':selected_course_id, 'course_user':course_user })
    else:
        return HttpResponseNotFound("<h1><center>Something went wrong!</center></h1>")





@login_required
def get_all_students(request):

    if request.user.is_superuser:
        all_students = Student.objects.all().order_by('first_name')
        return render(request , 'course_management/administration/students.html', {'students':all_students})

    if(hasattr(request.user , 'personal')):
        course_user = request.user.personal
    else:
        course_user = request.user.student 

    students = []
    for course in request.user.personal.course_set.all():
        for student in course.student_set.all().order_by('-first_name'):
            if student not in students:
                students.append(student)

    return render(request ,  'course_management/students.html', {'course_user': course_user,'students':students})



@login_required
def details_of_course(request , id):
    
    course = Course.objects.get(id=id)

    if request.user.is_superuser:
        return render(request , 'course_management/administration/lesson_details.html', {'course':course})


    if(hasattr(request.user , 'personal')):
        course_user = request.user.personal
    else:
        course_user = request.user.student 
    
    return render(request , 'course_management/course_details.html', {'course':course, 'course_user':course_user})


# important 

# # Create a CourseTopic instance
# topic = CourseTopic.objects.create(week_no=1, topic='Introduction to Programming')

# # Add the topic to a Course instance
# course = Course.objects.get(pk=1)
# course.course_topics.add(topic)

@login_required
def home(request):
    
    DAYS_OF_WEEK_CHOICES = [
        'monday', 
        'tuesday', 
        'wednesday', 
        'thursday', 
        'friday' 
    ]
    LECTURE_START_TIMES = [
        ('09:00am','09:45am'),
        ('10:00am','10:45am'),
        ('11:00am','11:45am'),
        ('01:00pm','01:45pm'),
        ('02:00pm','02:45pm'),
        ('03:00pm','03:45pm'),
        ('04:00pm','04:45pm')
    ] 

    if(request.user.is_superuser):
        class_room1 = ClassRoom.objects.all().filter(course__class_no=1)
        class_room2 = ClassRoom.objects.all().filter(course__class_no=2)
        class_room3 = ClassRoom.objects.all().filter(course__class_no=3)
        class_room4 = ClassRoom.objects.all().filter(course__class_no=4)
        print(class_room2)
        return render(request, 'course_management/administration/class_programs.html' , {'class_room1':class_room1,'class_room2':class_room2,'class_room3':class_room3,'class_room4':class_room4,'lecture_times':LECTURE_START_TIMES , 'lecture_days':DAYS_OF_WEEK_CHOICES})

    if(hasattr(request.user , 'personal')):
        course_user = request.user.personal
    else:
        return HttpResponse("<center><h1>This page not available</h1></center>")

    

    class_room = ClassRoom.objects.all().filter(course__lecturer=request.user.personal)

    


    return render(request ,'course_management/course_schedule.html', {'class_room':class_room,'course_user':course_user, 'lecture_times':LECTURE_START_TIMES , 'lecture_days':DAYS_OF_WEEK_CHOICES})

@login_required
def courses_(request):
    year  = datetime.datetime.now().year
    
    selected=request.POST.get('semester_select')


    if hasattr(request.user, 'personal'):
        course_list = request.user.personal.course_set.all()
        course_user = request.user.personal
        
        if selected:
            if selected=='all':
                courses = request.user.personal.course_set.all()
            elif selected=='Fall Semester':
                courses = request.user.personal.course_set.filter(semester = selected)
            else :
                courses = request.user.personal.course_set.filter(semester = selected)
        else:
            courses=request.user.personal.course_set.all()
            
    else:
        course_list = request.user.student.course_set.all()
        course_user = request.user.student
        
        if selected:
            if selected=='all':
                courses = request.user.student.course_set.all()
            elif selected=='Fall Semester':
                courses = request.user.student.course_set.filter(semester = selected)
            else :
                courses = request.user.student.course_set.filter(semester = selected)
        else:
            courses=request.user.student.course_set.all()
    return render(request ,  'course_management/courses.html' , { 'course_user':course_user,'course_list':course_list, 'courses':courses,'selected':selected , 'year':year})

def entry(request):
    return render(request , 'course_management/entry_page.html' , {})