from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    Choices=[
        ('student','Student'),
        ('tutor','Tutor'),
        ('admin','Admin'),
    ]
    role = models.CharField(max_length=8, choices=Choices)

    def __str__(self):
        return self.username

class Student(models.Model):
    first_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50, null = True, blank=True)        
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.CharField(max_length=100, null=True)
    year_of_study = models.PositiveIntegerField(blank=False)
    rewardPoints = models.PositiveIntegerField(default=0)
    courses_enrolled = models.ManyToManyField('Course' ,through='CourseEnrollment',through_fields=("student", "course"),blank=True, related_name='enrolled_students')
    def __str__(self) :
        return self.first_name

    def update_rewardPoints(self):
        assessment = StudentAssessment.objects.get(user = self.user)


class Tutor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)    
    specialization = models.TextField(null=True)
    department = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.first_name

    def get_course_count(self):
        return Course.objects.filter(tutor=self.user).count()

    def get_specializations(self):
        return self.specialization.split(",")

    def get_average_rating(self):
        courses = Course.objects.filter(tutor=self.user) 
        total_ratings = 0
        total_sum = 0
        rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for course in courses:
            course_ratings = course.ratings.all()
            for rating in course_ratings:
                rating_value = rating.rating
                total_sum += rating_value
                total_ratings += 1
                if rating_value in rating_counts:
                    rating_counts[rating_value] += 1

        if total_ratings == 0:
            return {
                "average_rating": None,
                "total_count": 0,
                "rating_counts": rating_counts
            }

        avg_rating = total_sum / total_ratings

        return {
            "average_rating": avg_rating,
            "total_count": total_ratings,
            "rating_counts": rating_counts
        }

class Course(models.Model):
    image = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=30, null=True, blank=True)
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) :
        return self.title

    def get_student_count(self):
        enrollment = CourseEnrollment.objects.filter(course = self)
        return enrollment.count()

    def get_section_count(self):
        return Section.objects.filter(course = self).count()

    def total_duration(self):
        sections = Section.objects.filter(course = self)
        return sum(section.duration or 0 for section in sections) or 0

    def save(self, *args, **kwargs):
        self.duration = self.total_duration()
        super().save(*args, **kwargs)

    def get_lesson_count(self):
        sections = Section.objects.filter(course = self)
        return sum(section.lesson.count() for section in sections)

    def get_average_rating(self):
        ratings = self.ratings.all()  

        if not ratings.exists():
            return {
                "average_rating": None,
                "total_count": 0,
                "rating_counts": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }

        rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_ratings = 0
        total_sum = 0

        for rating in ratings:
            rating_value = rating.rating
            total_sum += rating_value
            total_ratings += 1

            if rating_value in rating_counts:
                rating_counts[rating_value] += 1

        avg_rating = total_sum / total_ratings

        return {
            "average_rating": avg_rating,
            "total_count": total_ratings,
            "rating_counts": rating_counts
        }

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='section')
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self) :
        return self.title

    def total_duration(self):
        lessons = Lesson.objects.filter(section = self)
        return sum(lesson.duration or 0 for lesson in lessons) or 0

    def save(self, *args, **kwargs):
        self.duration = self.total_duration()
        super().save(*args, **kwargs)


class Lesson(models.Model):
    Choices=[
        ('reading','Reading'),
        ('video','Video'),
    ]
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lesson')
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=10, choices=Choices, null=True)
    content = models.CharField(max_length=1000 ,null = True, blank = True)
    def __str__(self) :
        return self.title

class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='students')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    validity = models.BooleanField(default=True)

class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.content

class CourseRating(models.Model):
    course = models.ForeignKey('Course', related_name='ratings', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('course', 'student')  

    def __str__(self):
        student_name = self.student.first_name if self.student.first_name else "Unnamed Student"
        return f"{self.course.title} - {student_name} Rating: {self.rating}"
        

class Todo(models.Model):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    category = models.CharField(max_length=20, null=True)
    created_on = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self) :
        return self.content

class Assessment(models.Model):
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def get_total_questions(self):
        return Question.objects.filter(assessment = self).count()

    def get_total_marks(self):
        questions = Question.objects.filter(assessment = self)
        return sum(question.marks or 0 for question in questions )

    def __str__(self):
        return self.title 

class Question(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE , related_name='questions')
    question = models.CharField(max_length=255,default="")
    options = models.CharField(max_length=255,null=True)
    answer = models.CharField(max_length=255,null=True)
    marks = models.PositiveIntegerField(null=True)

    def get_options(self):
        ops = self.options.split(',')
        options = {idx + 1 : option.strip() for idx, option in enumerate(ops)}
        return options

    def __str__(self):
        return self.question

class StudentAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(null=True, blank=True) 

    def __str__(self):
        return f"{self.student} - {self.assessment} - Score: {self.score}"

class Reward(models.Model):
    Choices=[
        ('shoes','Shoes'),
        ('books','Books'),
        ('vouchers','Gift Cards & Vouchers'),
        ('merchandise','Merchandise'),
        ('tech','Tech'),
        ('health','Health & Wellness')
    ]
    category = models.CharField(max_length=11, null=True, blank=True, choices=Choices)
    productName = models.CharField(max_length=100)
    productImage = models.CharField(max_length=255, null=True, blank=True)
    productPrice = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.productName
    