from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ChangePasswordView, CommentView, CourseView, EnrollCourseView, EnrolledStudentsView, LessonView, SectionView, Sectionview,StudentView, StudentProfileView, TodoView, TutorProfileView, TutorView, UserView, EnrolledView
from lms.views import LogoutView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'user', UserView)
router.register(r'student', StudentView)
router.register(r'tutor', TutorView)
router.register(r'courses', CourseView)
router.register(r'todo', TodoView)
router.register(r'section', SectionView)

urlpatterns = [
    path('',include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('student-profile/', StudentProfileView.as_view(), name='student_profile'),
    path('tutor-profile/', TutorProfileView.as_view(), name='tutor_profile'),
    path('enrolled-courses/', EnrolledView.as_view(), name='enrolled'),
    path('courses/<int:course_id>/enroll/', EnrollCourseView.as_view(), name='enroll'),
    path('courses/<int:course_id>/comments/', CommentView.as_view(), name='comments'),
    path('courses/<int:course_id>/students/', EnrolledStudentsView.as_view(), name="enrolled_students"),
    path('courses/<int:course_id>/sections/', Sectionview.as_view(), name='sections'),
    path('courses/<int:course_id>/sections/<int:section_id>/lessons/', LessonView.as_view(), name='lessons'),
]