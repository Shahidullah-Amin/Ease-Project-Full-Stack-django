from django.db import models
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
import datetime


class Faculty(models.Model):
    faculty_name = models.CharField(max_length=400)

    def __str__(self):
        return self.faculty_name


class Department(models.Model):
    department_name = models.CharField(max_length=400) 

    @property
    def number_of_students(self):
        return Student.objects.all().count()
    
    def __str__(self):
        return self.department_name
    
class Resource(models.Model):
    name = models.CharField(max_length=255 )
    reference = models.CharField(max_length=255)
    reference_address = models.URLField()

    def __str__(self):
        return self.reference_address
    

class CourseStructure(models.Model):
    math_science = models.IntegerField(default=0)
    engineering_science= models.IntegerField(default=0)
    engineering_design = models.IntegerField(default=0)
    liberal_arts = models.IntegerField(default=0)
    educational_science = models.IntegerField(default=0)
    science = models.IntegerField(default=0)
    health_science = models.IntegerField(default=0)
    area_information = models.IntegerField(default=0)

    

class CourseOutcomes(models.Model):
    outcome = models.TextField()

    def __str__(self):
        return self.outcome

class ClassRoom(models.Model):
    DAYS_OF_WEEK_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    LECTURE_START_TIMES = [
        ('09:00am-09:45am', '09:00am-09:45am'),
        ('10:00am-10:45am', '10:00am-10:45am'),
        ('11:00am-11:45am', '11:00am-11:45am'),
        ('01:00pm-01:45pm', '01:00pm-01:45pm'),
        ('02:00pm-02:45pm', '02:00pm-02:45pm'),
        ('03:00pm-03:45pm', '03:00pm-03:45pm'),
        ('04:00pm-04:45pm', '04:00pm-04:45pm'),
    ]
        
    
    course = models.ForeignKey('Course', related_name='class_room',on_delete=models.SET_NULL, null=True)
    room_no = models.CharField(max_length=100)
    day = models.CharField(choices=DAYS_OF_WEEK_CHOICES , max_length=30)
    lecture_time = models.CharField(choices=LECTURE_START_TIMES , max_length=50)

    def __str__(self) -> str:
        return self.course.course_name +"  "+self.room_no

    def clean(self):
        super().clean()

        existing_instances = ClassRoom.objects.filter(
            day=self.day,
            room_no=self.room_no,
            lecture_time=self.lecture_time
        ).exclude(pk=self.pk) 

        if existing_instances.exists():
            raise ValidationError(
                'Another Class with the same Teacher, Day, and same lecture start time already exists.'
            )



class Course(models.Model):

    
    course_language  = models.CharField(max_length=20 , choices=(('English','English') , ('Turkish','Turkish')), default='Turkish')
    course_level = models.CharField(max_length=200 , choices=(('associate degree','associate degree'),('licence','licence') , ('master degree','master degree'),('doc','doc')), default='licence')
    aim_of_lesson = models.TextField()
    course_content = models.TextField()
    course_assistants = models.ManyToManyField('Personal', related_name='assistants', blank=True)   
    course_resources  = models.ManyToManyField(Resource)   
    course_structure  = models.OneToOneField(CourseStructure , blank=True , null=True , on_delete=models.SET_NULL)
    course_learning_outcomes = models.ManyToManyField(CourseOutcomes)                                
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey( Department, on_delete=models.CASCADE)
    class_no= models.IntegerField( default=0 )
    course_code = models.CharField(max_length=15 , default="MYAZ230")
    course_name = models.CharField(max_length=400)
    lecturer = models.ForeignKey('Personal', on_delete= models.SET_NULL , null=True  , related_name='course_set')
    credit = models.IntegerField(default=0)
    course_topics = models.ManyToManyField('CourseTopic' , blank=True )
    midterm_exam = models.IntegerField(  validators=[MaxValueValidator(100)], default=40 ,blank=True)
    final_exam = models.IntegerField( validators=[MaxValueValidator(100)], default=60 ,blank=True, null=True)
    assginment = models.IntegerField( validators=[MaxValueValidator(100)] ,blank=True, null=True) 
    practice = models.IntegerField( validators=[MaxValueValidator(100)] ,blank=True, null=True)
    project = models.IntegerField( validators=[MaxValueValidator(100)] ,blank=True, null=True)
    course_document = models.FileField(upload_to='lesson_documents/',null=True)
    semester_choices=(
        ('Spring Semester', 'Spring Semester'),
        ('Fall Semester','Fall Semester')
    )
    semester = models.CharField(max_length=30 , choices=semester_choices , null=True , blank=True)
    _semester_choice = (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
    )
    semester_no = models.IntegerField(choices=_semester_choice , default=1)

    @property
    def number_of_students(self):
        return self.student_set.all().count()



    def __str__(self):
        return self.course_name
    

    def clean(self):
        total = (self.midterm_exam or 0)+ (self.final_exam or 0)+(self.assginment or 0) + (self.practice or 0 ) + (self.project or 0 )

        if total != 100:
            raise ValidationError("The sum of exam weights must be equal to 100.")
    

class CourseTopic(models.Model):
    week_no = models.IntegerField(choices=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'),(13,'13'),(14,'14')))
    topic = models.CharField(max_length=255 )
    document = models.FileField(upload_to='course_plan_files' ,blank=True , null=True)

    def __str__(self):
        return self.topic


class Personal(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name='personal')
    faculty = models.ForeignKey(Faculty , on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    identity_no = models.IntegerField(unique=True)
    personal_no = models.CharField( max_length=10 , unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.first_name +" "+self.last_name
    
    def clean(self):
        if self.user is not None and hasattr(self.user, 'student'):
            raise ValidationError('User already associated with a student')
    

class Mark(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name='student_mark')
    course = models.ForeignKey(Course , on_delete=models.CASCADE , related_name='student_mark') 
    marks = models.IntegerField(validators=[MaxValueValidator(100)] , null=False , default=None)
    exam_doc = models.FileField(upload_to='exam_documents', null=True , blank=True)


    def __str__(self) -> str:
        return str(self.marks)

    @property
    def letter_grade(score):
        letter_grade = None
        if score >= 90:
            letter_grade = 'AA'
        elif score >= 85:
            letter_grade = 'BA'
        elif score >= 80:
            letter_grade = 'BB'
        elif score >= 75:
            letter_grade = 'cB'
        elif score >= 70:
            letter_grade = 'CC'
        elif score >= 60:
            letter_grade = 'DC'
        elif score >= 50:
            letter_grade = 'DD'
        else:
            letter_grade = 'FF'
        return letter_grade
 

    @property
    def score_to_letter_grade(score):
        letter_grade = None
        if score >= 90:
            letter_grade = 4.0
        elif score >= 85:
            letter_grade = 3.50
        elif score >= 80:
            letter_grade = 3.00
        elif score >= 75:
            letter_grade = 2.50
        elif score >= 70:
            letter_grade = 2.00
        elif score >= 60:
            letter_grade = 1.50
        elif score >= 50:
            letter_grade = 1.00
        elif score >=30:
            letter_grade = 0.50
        else:
            letter_grade = 0
        return letter_grade
 



class Student(models.Model):

    _class_choice = (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        (6,'6'),
        (7,'7')
    )

    user = models.OneToOneField(User , on_delete = models.CASCADE , related_name='student')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey( Department, on_delete=models.CASCADE)
    identity_no = models.IntegerField(unique=True)
    student_no = models.CharField( max_length=10, unique=True , default=f"{(str (datetime.datetime.now().year)[2:4] + str(datetime.datetime.now().month)+str(User.objects.all().count())):0>10}")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255 )
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    student_status = models.BooleanField(default=False)
    semester = models.IntegerField(default=0)
    class_no = models.IntegerField(choices=_class_choice)
    academic_advisor = models.ForeignKey(Personal , on_delete=models.SET_NULL , null=True, blank=True)
    courses = models.ManyToManyField(to=Course , related_name='student_set')

    def __str__(self):
        return self.first_name+" "+self.last_name
    

    
    def clean(self):
        if self.user is not None and hasattr(self.user, 'personal'):
            raise ValidationError('User already associated with a personal')

