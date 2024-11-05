from dataclasses import fields
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from lms.models import Comment, Course, CourseEnrollment, Lesson, Section, Student, Todo, Tutor, User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','email','role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Student
        fields = ['user','username','first_name','last_name','program','year_of_study','courses_enrolled']
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Student.objects.create(user = user, **validated_data)

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['user','first_name','last_name','specialization','department','years_of_experience','bio',]
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Tutor.objects.create(user=user, **validated_data)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course        
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer
    class Meta:
        model = Section
        fields = '__all__'  
        read_only_fields = ['id','course'] 

class LessonSerialzer(serializers.ModelSerializer):
    section = SectionSerializer
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['id','section']     

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only = True)
    class Meta:
        model = CourseEnrollment
        fields = ['id', 'enrollment_date', 'validity', 'course'] 

class CommmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['course', 'user', 'created_at']

class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['id','user','created_on']
