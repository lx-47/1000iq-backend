from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    Choices=[
        ('student','Student'),
        ('tutor','Tutor'),
        ('admin','Admin'),
    ]
    role = models.CharField(max_length=8, choices=Choices)

    def __str__(self):
        return self.username

class Student(models.Model):
    first_name = models.CharField(max_length = 50, null = True)
    last_name = models.CharField(max_length = 50, null = True)        
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.CharField(max_length=100, null=True)
    year_of_study = models.PositiveIntegerField(blank=False)
    courses_enrolled = models.ManyToManyField('Course' ,through='CourseEnrollment',through_fields=("student", "course"),blank=True, related_name='enrolled_students')

class Tutor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    bio = models.TextField(blank=True, null=True)

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(blank=True, null=True)

class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    validity = models.BooleanField(default=True)