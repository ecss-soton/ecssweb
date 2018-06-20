from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=20)

class Feedback(models.Model):
    message = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # Time when the feedback submitted
    time = models.DateField(auto_now_add=True)
    # Record if a committee member submitted the feedback
    committee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

class Response(models.Model):
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE)
    message = models.TextField()
    committee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now=True)
