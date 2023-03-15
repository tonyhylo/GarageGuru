from django.db import models

class Post(models.Model):
    description = models.TextField(max_length=10000)