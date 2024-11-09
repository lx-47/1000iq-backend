from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    AssessmentViewSet, 
    ChangePasswordView, 
    CommentView, 
    CourseView, 
    EnrollCourseView, 
    EnrolledStudentsView, 
    LessonView, 
    RatingView,
    RewardView, 
    SectionView, 
    Sectionview,
    StudentAssessmentViewSet, 
    StudentView, 
    StudentProfileView, 
    TodoView, 
    TutorProfileView, 
    TutorView, 
    UserView, 
    EnrolledView
)
from lms.views import LogoutView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'user', UserView)
router.register(r'student', StudentView)
router.register(r'tutors', TutorView)
router.register(r'courses', CourseView)
router.register(r'todo', TodoView)
router.register(r'sections', SectionView)    
router.register(r'reward', RewardView)
course_rating_create = RatingView.as_view({
    'post': 'create',
    'get':'list',
})

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
    path('sections/<int:section_id>/assessments/', AssessmentViewSet.as_view({'get': 'list'})),
    path('assessments/<int:assessment_id>/reports/', StudentAssessmentViewSet.as_view(), name='reports'),
    path('courses/<int:course_id>/rating/', course_rating_create, name='course-rating-create'),
]