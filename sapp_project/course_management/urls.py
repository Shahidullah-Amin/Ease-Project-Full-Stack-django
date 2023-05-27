from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('' , views.entry , name='login_entry'),
    path('administration/delete-class/<int:id>' , views.delete_class , name='delete-class'),
    path('administration/edit-class/<int:id>' , views.edit_class , name='edit-class'),
    path('administration/add-class' , views.add_class , name='add-class'),
    path('administration/all-classes' , views.get_classes , name='all-classes'),
    path('administration/delete-lesson/<int:id>' , views.delete_lesson , name='delete-lesson'),
    path('administration/edit-lesson/<int:id>' , views.edit_lesson , name='edit-lesson'),
    path('administration/add-lesson' , views.add_lesson , name='add-lesson'),
    path('administration/lessons' , views.get_all_lessons , name='lessons'),
    path('administration/delete-confirm/<int:id>' , views.delete_confirmation , name='delete-confirm'),
    path('administration/delete-teacher/<int:id>' , views.delete_teacher , name='delete-teacher'),
    path('administration/edit-teacher/<int:id>' , views.edit_teacher , name='edit-teacher'),
    path('administration/add-teacher' , views.add_teacher , name='add-teacher'),
    path('administration/teachers' , views.get_all_teachers , name='teachers'),
    path('administration/not-found' , views.notfound , name='notfound'),
    path('evaluate-student-score', views.evaluate_student , name = 'evaluate-student-score'),
    path('evaluate-student-score/<int:id>', views.evaluate_student , name = 'evaluate-student-score'),
    path('add-topic', views.add_topic , name = 'add-topic'),
    path('remove-topic/<int:id>', views.remove_topic , name = 'remove-topic'),
    path('add-topic/<int:id>', views.add_topic , name = 'add-topic'),
    path('add-topic/<int:id>', views.add_topic , name = 'add-topic'),
    path('mark-contribution/<int:id>', views.mark_cotribution , name = 'mark-contribution'),
    path('students', views.get_all_students , name = 'students'),
    path('courses-all' , views.courses_ , name = 'courses'),
    path('home' , views.home , name = 'home'),
    path('course-info/<int:id>' , views.details_of_course , name = 'course-info'),
    path('evaluate-lessons' , views.evaluate_course , name='evaluate-lessons'),
    path('user_login/', auth_views.LoginView.as_view(template_name='course_management/user_login.html') , name='user-login'),
    path('logout/', auth_views.LogoutView.as_view() , name='logout'),

]