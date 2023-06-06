from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Explanation(models.Model):
    explanation = models.TextField(default='')

class Threads(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_path = models.CharField(max_length=200, default='')
    edited_csv_path = models.CharField(max_length=200, default='')
    slug = models.SlugField(default='')
    title = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(default=timezone.now)
    expl_enable = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

class Message(models.Model):
    thread = models.ForeignKey(Threads, on_delete=models.CASCADE)
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, default='')
    content_path = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(default=timezone.now)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)