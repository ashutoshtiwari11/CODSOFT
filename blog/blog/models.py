from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    fr_ky = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone = models.CharField(max_length=12)
    Bio = models.CharField(max_length = 100)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to='profile_images/', default="")
    content = models.CharField(max_length=5000)
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(auto_now=True)



