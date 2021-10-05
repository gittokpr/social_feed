from django.db import models
from djongo import models as dmodels

# FbPosts model saved in remote db


class FbPosts(models.Model):
    postId = models.CharField(max_length=100, unique=True)
    userName = models.CharField(max_length=40)
    userId = models.CharField(max_length=100)
    postDescription = models.TextField(max_length=5000, null=True)
    postImage = models.TextField(max_length=5000, null=True)
    created_at = models.DateTimeField()

# post object saved in mongodb cloud


class Post(dmodels.Model):
    postId = dmodels.CharField(max_length=100, primary_key=True)
    postDescription = dmodels.TextField(max_length=5000, null=True)
    postImage = dmodels.TextField(max_length=5000, null=True)
    created_at = dmodels.DateTimeField()
    # workaround for object is not subscriptable error

    def __getitem__(self, name):
        return getattr(self, name)

# fbObject saved in mongodb cloud


class FbObject(dmodels.Model):
    userName = dmodels.CharField(max_length=100)
    userId = dmodels.CharField(max_length=100, primary_key=True)
    posts = dmodels.ArrayField(model_container=Post)
