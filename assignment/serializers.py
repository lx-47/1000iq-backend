from django.utils import timezone
from urllib import request
from rest_framework import serializers
from .models import Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'student', 'tutor', 'title', 'description', 'due_date', 'created_at', 'is_completed', 'answer']
        read_only_fields = ['id', 'created_at', 'tutor', 'is_completed']       

    def validate(self, data):
        user = self.context['request'].user
        if user.role != 'tutor' and self.context['request'].method in ['POST','PUT','DELETE','PATCH']:
            raise serializers.ValidationError("Only tutors can create, update, or delete assignments.")
        if user.role == 'student' and 'answer' in data:
                data.pop('student', None)  # Prevent students from changing the 'student' field
        return data

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['answer', 'submission_date']
        read_only_fields = ['submission_date']

    def update(self, instance, validated_data):
        instance.answer = validated_data.get('answer', instance.answer)
        instance.submission_date = timezone.now()
        instance.save()
        return instance        