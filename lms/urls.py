from unicodedata import name
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import StudentProfile, TutorProfile, UserView

router = DefaultRouter()
router.register(r'user', UserView)
router.register(r'student', StudentProfile)
router.register(r'tutor', TutorProfile)

urlpatterns = [
    path('',include(router.urls)),
]