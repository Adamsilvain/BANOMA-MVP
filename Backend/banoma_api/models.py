from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    skills = models.CharField(max_length=200)
    languages = models.CharField(max_length=200)
    credibility_score = models.FloatField(default=0.0)

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
