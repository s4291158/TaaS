from django.db import models
from django.contrib.auth.models import User


class Session(models.Model):
    key = models.CharField(max_length=40)

    def __str__(self):
        return str(self.id)


class Idea(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    name = models.CharField(max_length=40)
    description = models.TextField()
    email = models.EmailField(null=True, blank=True)

    valid = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Like(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

    liked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
