from django.db import models
from django.contrib.auth.models import User

    
class Course(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    cate = models.CharField(max_length=50)
    desc = models.CharField(max_length=5000)
    link = models.URLField()
    img = models.ImageField(upload_to='secure_data/')
    video_link = models.URLField()
    duration = models.IntegerField()
    author = models.CharField(max_length=100)    
    author_details = models.CharField(max_length=1000)
    cost = models.IntegerField()
    

class Quiz(models.Model):
    fr_ky = models.ForeignKey(Course, on_delete=models.CASCADE)
    data = models.FileField(upload_to='quizz_data/')
    study_material = models.FileField(upload_to='study_materials/')

accnt = [
        ('student', 'Student'),
        ('content creator', 'content creator'),
    ]

from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    fr_ky = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    img = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    typeofaccount = models.CharField(max_length=20, default='A')
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fname} {self.lname}"





class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    # You can add more fields to track progress, such as quiz scores, completion percentage, etc.

    