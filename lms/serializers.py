from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from lms.models import Student, Tutor, User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','password','email','role']
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['program','year_of_study']

    def create(self, validated_data):
        user = self.context['request'].user
        return Student.objects.create(user=user, **validated_data)

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['specialization','department','years_of_experience','bio',]
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Tutor.objects.create(user=user, **validated_data)