from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
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
    User 
    )
from lms.serializers import ( 
    AssessmentSerializer, 
    ChangePasswordSerializer, 
    CommmentSerializer, 
    CourseEnrollmentSerializer, 
    CourseRatingSerializer, 
    CourseSerializer, 
    CourseSerializer2, 
    LessonSerializer, 
    QuestionSerializer, 
    RewardSerializer, 
    SectionSerializer,
    StudentAssessmentSerializer, 
    StudentSerializer, 
    TodoSerializer, 
    TutorSerializer, 
    UserSerializer
    )
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)           

class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        self.object = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)

class StudentProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def get_object(self):
        return Student.objects.get(user = self.request.user)
    
class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class TutorView(ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer 
    permission_classes = [IsAuthenticated]

class CourseView(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer2
    permission_classes = [IsAuthenticated]
    filter_backends=[SearchFilter]
    search_fields = ['title','category','description']

class RatingView(ModelViewSet):
    serializer_class = CourseRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseRating.objects.filter(student__user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Get the course ID from the URL
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        
        # Ensure the rating is unique for this student and course
        if CourseRating.objects.filter(course=course, student__user=request.user).exists():
            return Response({"detail": "You have already rated this course."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a rating
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course, student=request.user.student)  # Use the related student instance
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#To view all the courses a student has enrolled in
class EnrolledView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        try:
            student = user.student
        except Student.DoesNotExist:
            return Response({'detail':'User is not a student'}, status=status.HTTP_403_FORBIDDEN)

        enrollments = CourseEnrollment.objects.filter(student=student)
        serializer = CourseEnrollmentSerializer(enrollments, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#To view all students enrolled in a course
class EnrolledStudentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id = course_id)
        except Course.DoesNotExist:
            return Response({'detail':'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        enrollments = CourseEnrollment.objects.filter(course = course)
        students = [enrollment.student for enrollment in enrollments]
        serializer = StudentSerializer(students, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#To enroll in a course
class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, course_id):
        user = request.user
        try:
            student = user.student
        except Student.DoesNotExist:
            return Response({'detail': 'User is not a student'}, status=status.HTTP_403_FORBIDDEN)
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        if CourseEnrollment.objects.filter(student=student, course=course).exists():
            return Response({'detail': 'Already enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
        enrollment = CourseEnrollment.objects.create(student=student, course=course)
        
        return Response({
            'id': enrollment.id,
            'course': enrollment.course.id,
            'enrollment_date': enrollment.enrollment_date,
            'validity': enrollment.validity
        }, status=status.HTTP_201_CREATED)



#to add commments under a course
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id):
        comments = Comment.objects.filter(course_id = course_id)
        serializer = CommmentSerializer(comments, many = True)
        return Response(serializer.data)

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            Response({'detail':'Course not found.'},status=status.HTTP_404_NOT_FOUND)    
        serialzer = CommmentSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save(course = course, user = request.user)
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)   

class TodoView(ModelViewSet):
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    def get_queryset(self):
        return Todo.objects.filter(user = self.request.user)
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)    

class SectionView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class Sectionview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id):
        section = Section.objects.filter(course_id = course_id)
        serializer = SectionSerializer(section, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id = course_id)
        except Course.DoesNotExist:
            Response({'detail':'Course not found.'},status=status.HTTP_404_NOT_FOUND)    
        serialzer = SectionSerializer(data = request.data)
        if serialzer.is_valid():
            serialzer.save(course = course)
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)            

class LessonView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, section_id, *args, **kwargs):

        lesson = Lesson.objects.filter(section_id = section_id)
        serializer = LessonSerializer(lesson, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, section_id,  *args, **kwargs):
        try:
            section = Section.objects.get(id = section_id)
        except Section.DoesNotExist:
            Response({'detail':'Section not found.'},status=status.HTTP_404_NOT_FOUND)    
        serialzer = LessonSerializer(data = request.data)
        if serialzer.is_valid():
            serialzer.save(section = section)
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class AssessmentViewSet(ReadOnlyModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs.get('section_id')
        return Assessment.objects.filter(section_id=section_id, is_active=True)

class StudentAssessmentViewSet(RetrieveUpdateAPIView):
    serializer_class = StudentAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        assessment_id = self.kwargs['assessment_id']
        return StudentAssessment.objects.get(user=self.request.user, assessment_id=assessment_id)

class RewardView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    filter_backends=[SearchFilter]
    search_fields = ['category']
