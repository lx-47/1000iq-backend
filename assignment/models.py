from django.db import models
from django.conf import settings
# Create your models here.
class Assignment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role':'student'}, related_name='assignments')
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role':'tutor'}, related_name='created_assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    submission_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.student.username}"    