from pickle import TRUE
from random import choices
from tkinter import CASCADE
from turtle import title
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
    first_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50, null = True, blank=True)        
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.CharField(max_length=100, null=True)
    year_of_study = models.PositiveIntegerField(blank=False)
    courses_enrolled = models.ManyToManyField('Course' ,through='CourseEnrollment',through_fields=("student", "course"),blank=True, related_name='enrolled_students')

class Tutor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 50, null = True)
    last_name = models.CharField(max_length = 50, null = True)    
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    bio = models.TextField(blank=True, null=True)

class Course(models.Model):
    image = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(blank=True, null=True)

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

class Lesson(models.Model):
    Choices=[
        ('reading','Reading'),
        ('video','Video'),
    ]
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=10, choices=Choices, null=True)
    content = models.CharField(max_length=1000 ,null = True, blank = True)


class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    validity = models.BooleanField(default=True)

class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Todo(models.Model):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)