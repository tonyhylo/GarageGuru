from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
import uuid
import boto3
from .models import Post, Photo, Comment
from .forms import CommentForm

# Auth
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView




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
  comment_form = CommentForm()
  return render(request, 'posts/detail.html', { 'post': post, 'comment_form': comment_form })

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

def delete_photo(request, post_id, photo_id):
   photo = Photo.objects.get(id=photo_id)
   photo.delete()
   return redirect('detail', post_id=post_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = '__all__'
  success_url = '/'

  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('detail', kwargs={'post_id': self.id})
  
  def form_valid(self, form):
    form.instance.user = self.request.user  
    return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = '__all__'
  success_url = '/'


class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/'


@login_required
def add_comment(request, post_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.post_id = post_id
    new_comment.save()
  return redirect('detail', post_id=post_id)

@login_required
def delete_comment(request, post_id, comment_id):
  comment = Comment.objects.get(id=comment_id)
  comment.delete()
  return redirect('detail', post_id=post_id)


@login_required
def post_index(request):
  post = post.objects.filter(user=request.user)
  return render(request, 'post/index.html', {'posts': post})


@login_required
def posts_detail(request, post_id):
  post = post.objects.get(id=post_id)
  return render(request, 'post/detail.html', {
      'post': post, 
  })

@login_required
def add_photo(request, post_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, post_id=post_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', post_id=post_id)
