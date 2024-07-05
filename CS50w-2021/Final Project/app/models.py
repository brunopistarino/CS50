from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Projects(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, related_name="project_owner", on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="project_members")
    color = models.IntegerField()

class Tasks(models.Model):
    name = models.CharField(max_length=128)
    project = models.ForeignKey(Projects, related_name="tasks_project", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="tasks_members", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date = models.DateField()

class Chats(models.Model):
    user = models.ForeignKey(User, related_name="chat_user", on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, related_name="chat_project", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=256)