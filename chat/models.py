from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Threads(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_path = models.CharField(max_length=200, default='')
    edited_csv_path = models.CharField(max_length=200, default='')
    slug = models.SlugField(default='')
    title = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(default=timezone.now)

class Message(models.Model):
    thread = models.ForeignKey(Threads, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='')
    content_path = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(default=timezone.now)