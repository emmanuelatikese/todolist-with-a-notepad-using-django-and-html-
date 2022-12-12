from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Todo(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self): return self.title
    
    class Meta:ordering = ['-created', '-updated']
    
class Notepad(models.Model):
    title = models.CharField(max_length=225)
    body = models.TextField(blank=True, null=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateField(auto_now=True)
    