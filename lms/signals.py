from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CourseEnrollment

@receiver(post_save, sender=CourseEnrollment)
def add_course_to_student_enrolled_courses(sender, instance, created, **kwargs):
    if created and instance.validity: 
        instance.student.courses_enrolled.add(instance.course)

@receiver(post_delete, sender=CourseEnrollment)
def remove_course_from_student_enrolled_courses(sender, instance, **kwargs):
    instance.student.courses_enrolled.remove(instance.course)
