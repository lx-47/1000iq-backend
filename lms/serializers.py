from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from lms.models import (
    Assessment,
    Comment, 
    Course,
    CourseEnrollment,
    CourseRating, 
    Lesson,
    Question,
    Reward, 
    Section, 
    Student,
    StudentAssessment, 
    Todo, 
    Tutor, 
    User,
)

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

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.password = make_password(new_password)
        user.save()

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Student
        fields = ['user','image','banner','username','email','first_name','last_name','rewardPoints','courses_enrolled']
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Student.objects.create(user = user, **validated_data)

class TutorSerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()
    specializations = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Tutor
        fields = ['id','user','email','first_name','last_name','image','banner','department','years_of_experience','bio','course_count','specializations','average_rating',]
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Tutor.objects.create(user=user, **validated_data)
    def get_course_count(self, obj):
        return obj.get_course_count()  
    def get_specializations(self,obj):
        return obj.get_specializations()  
    def get_average_rating(self, obj):
        return obj.get_average_rating()        

class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRating
        fields = ['id']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course        
        fields = ['id','image','title','description','category','tutor']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['id'] 

class SectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer
    lesson = LessonSerializer(many = True)
    class Meta:
        model = Section
        fields = ['id','title','duration','lesson']  
        read_only_fields = ['id','course','lesson']

class CourseSerializer2(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only = True)
    average_rating = serializers.SerializerMethodField() 
    section_count = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    student_ids = serializers.SerializerMethodField()
    tutor = TutorSerializer
    class Meta:
        model = Course
        fields = ['id', 'image','title', 'description','category', 'tutor' , 'duration' ,'section_count', 'lesson_count','student_count','student_ids','average_rating', 'sections'] 

    def get_average_rating(self, obj):
        return obj.get_average_rating()
    def get_section_count(self, obj):
        return obj.get_section_count()
    def get_lesson_count(self, obj):
        return obj.get_lesson_count() 
    def get_student_count(self, obj):
        return obj.get_student_count()
    def get_student_ids(self, obj):
        return obj.get_student_ids()
           

    
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only = True)
    class Meta:
        model = CourseEnrollment
        fields = ['id','enrollment_date', 'validity', 'course']

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
        read_only_fields = ['id','user']


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ['id', 'question', 'question', 'marks','options','answer']

    def get_options(self, obj):
        return obj.get_options()    

class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many = True)
    total_marks = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    class Meta:
        model = Assessment
        fields = ['id', 'title','total_questions', 'total_marks', 'questions']

    def get_total_marks(self, obj):
        return obj.get_total_marks()
    def get_total_questions(self, obj):
        return obj.get_total_questions()        

class StudentAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAssessment
        fields = ['id', 'is_completed', 'score']

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id','category','productName','productImage','productPrice']
