from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from lms.models import Student, Tutor, User
from lms.serializers import StudentSerializer, TutorSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    

class StudentProfile(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TutorProfile(ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer 
    permission_classes = [IsAuthenticated]
