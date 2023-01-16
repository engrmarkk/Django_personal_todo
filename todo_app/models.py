from django.db import models
# from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Todo(models.Model):
    todo = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.todo
