from datetime import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status,permissions
from rest_framework.response import Response
from .models import Assignment
from .serializers import AssignmentSerializer, StudentAnswerSerializer
from django.core.exceptions import PermissionDenied
# Create your views here.
class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Assignment.objects.filter(student=user)
        elif user.role == 'tutor':
            return Assignment.objects.filter(tutor=user)
        return Assignment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'tutor':
            serializer.save(tutor=user)
        else:
            raise permissions.PermissionDenied("Only tutors can create assignments.")

    def update(self, request, *args, **kwargs):
        user = request.user
        assignment = self.get_object()

        if user.role == 'student' and 'answer' in request.data:
            if assignment.student != user:
                return Response({'error': 'You can only upload answers to your own assignments.'}, status=status.HTTP_403_FORBIDDEN)
            if assignment.due_date < timezone.now():
                return Response({'error': 'Assignment deadline has passed.'}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.get_serializer(assignment, data={'answer': request.data['answer']}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif user.role == 'tutor':
            return super().update(request, *args, **kwargs)
        else:
            return Response({'error': 'Only tutors can update assignments.'}, status=status.HTTP_403_FORBIDDEN)       

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'tutor':
            return Response({'error': 'Only tutors can delete assignments.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)  


class StudentAnswerView(APIView):      
    permission_classes = [IsAuthenticated]
    def patch(self, request, assignment_id):
        user = request.user

        if user.role != 'student':
            raise PermissionDenied('Only students can sumbit answers')       
        try:
            assignment = Assignment.objects.get(id=assignment_id, student=user)
        except Assignment.DoesNotExist:
            return Response({'error': 'Assignment not found or not assigned to this student.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentAnswerSerializer(assignment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                              