from django.db import models

class Post(models.Model):
    description = models.TextField(max_length=10000)
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for post_id: {self.post_id} @{self.url}"

class Comment(models.Model):
    comment = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)



