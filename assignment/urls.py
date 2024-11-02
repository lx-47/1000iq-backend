from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, StudentAnswerView

router = DefaultRouter()
router.register(r'assignments',AssignmentViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('assignments/<int:assignment_id>/submit-answer/', StudentAnswerView.as_view(), name='submit-answer'),

]