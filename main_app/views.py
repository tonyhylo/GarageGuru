from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse
from .models import Post


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