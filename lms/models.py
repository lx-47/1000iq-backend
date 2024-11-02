from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.CharField(max_length=100, null=True)
    year_of_study = models.PositiveIntegerField()
    #courses_enrolled = models.ManyToManyField('Course', blank=True)
    #friends = models.ManyToManyField('self', blank=True)

class Tutor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    bio = models.TextField(blank=True, null=True)