from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        TEACHER = 'TEACHER', 'Teacher'
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    class Meta:
        unique_together = ('student', 'date')
    def __str__(self):
        return f"{self.student.username} - {self.date}: {self.status}"