from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Post(models.Model):
    description = models.TextField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for post_id: {self.post_id} @{self.url}"

class Comment(models.Model):
    comment = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
    
    


