from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Course, CourseEnrollment, Student, Tutor, User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            "fields": (
                'role',
            ),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": (
                'role',
            )
        }),
    )
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(CourseEnrollment)