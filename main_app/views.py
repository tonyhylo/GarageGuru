from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
import uuid
import boto3
from .models import Post, Photo

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'garageguru57'

def home(request):
  posts = Post.objects.all()
  return render(request, 'home.html', { 'posts': posts })
  # return render(request, 'home.html')

def messages(request):
  return render(request, 'messages.html')

def profile(request):
  return render(request, 'profile.html')

def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  return render(request, 'posts/detail.html', { 'post': post })

def add_photo(request, post_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = 'garageguru/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            Photo.objects.create(url=url, post_id=post_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', post_id=post_id)


class PostCreate(CreateView):
  model = Post
  fields = '__all__'
  success_url = '/'

  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('detail', kwargs={'post_id': self.id})

class PostUpdate(UpdateView):
  model = Post
  fields = '__all__'
  success_url = '/'

class PostDelete(DeleteView):
  model = Post
  success_url = '/'