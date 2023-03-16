from django.db import models

class Post(models.Model):
    description = models.TextField(max_length=10000)

class Comment(models.Model):
    comment = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)



