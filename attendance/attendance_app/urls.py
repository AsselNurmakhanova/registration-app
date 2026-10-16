from django.urls import path
from . import views

urlpatterns = [
    path('', views.mark_attendance, name='mark_attendance'),
    path('records/', views.attendance_list, name='attendance_list'),
    path('signup/', views.signup_view, name='signup'),
    path('student/add/', views.add_student, name='add_student'), 
    path('student/delete/<int:student_id>/', views.delete_student, name='delete_student'),
]