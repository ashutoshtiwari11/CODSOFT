from django.contrib import admin
from .models import Course, Quiz, Progress, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Customize the admin view for CustomUser if needed
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Customize the admin view for Course if needed
    pass

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    # Customize the admin view for Quiz if needed
    pass

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    # Customize the admin view for Progress if needed
    pass
