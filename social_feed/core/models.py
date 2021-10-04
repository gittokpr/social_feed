from django.db import models
from djongo import models as dmodels


class FbPosts(models.Model):
    postId = models.CharField(max_length=100, unique=True)
    userName = models.CharField(max_length=40)
    userId = models.CharField(max_length=100)
    postDescription = models.TextField(max_length=5000, null=True)
    postImage = models.TextField(max_length=5000, null=True)
    created_at = models.DateTimeField()


class Post(dmodels.Model):
    postId = dmodels.CharField(max_length=100, primary_key=True)
    postDescription = dmodels.TextField(max_length=5000)
    postImage = dmodels.TextField(max_length=5000)
    created_at = dmodels.DateTimeField()


class FbObject(dmodels.Model):
    userName = dmodels.CharField(max_length=100)
    userId = dmodels.CharField(max_length=100, primary_key=True)
    posts = dmodels.ArrayField(model_container=Post)
