from django.shortcuts import render
from django.contrib import messages as django_messages
from django.shortcuts import render, redirect
from .models import Message
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

import uuid
import boto3

from .models import Post, Photo, Comment, Like, User, UserDescription
from .forms import CommentForm

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'garageguru57'

def home(request):
  posts = Post.objects.all()
  return render(request, 'home.html', { 'posts': posts })


@login_required
def messages(request):
  return render(request, 'messages.html')


@login_required
def profile(request, user_id):
  posts = Post.objects.filter(user=user_id)
  user_profile = User.objects.filter(id = user_id).values()[0]
  bio = UserDescription.objects.filter(user_id=user_id).values()[0]
  return render(request, 'profile.html', {'posts': posts, 'user_profile': user_profile, 'bio':bio})


@login_required
def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  comment_form = CommentForm()
  return render(request, 'posts/detail.html', { 'post': post, 'comment_form': comment_form })


@login_required
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


@login_required
def delete_photo(request, post_id, photo_id):
   photo = Photo.objects.get(id=photo_id)
   photo.delete()
   return redirect('detail', post_id=post_id)


def search_by_hashtag(request, hashtag):
    posts = Post.objects.filter(description__icontains=f'#{hashtag}')

    context = {
        'hashtag': hashtag,
        'posts': posts,
    }
    return render(request, 'search_results.html', context)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['description']
  success_url = '/'

  def __str__(self):
    return self.name
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
    
  def get_absolute_url(self):
    return reverse('detail', kwargs={'post_id': self.id})


class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = '__all__'
  success_url = '/'

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/'


@login_required
def messages(request):
    received_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messages.html', {'messages': received_messages})


# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         recipient = User.objects.get(username=request.POST['recipient'])
#         content = request.POST['content']
#         message = Message(sender=request.user,
#                           recipient=recipient, content=content)
#         message.save()
#         return redirect('messages')
#     return render(request, 'send_message.html')


@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_username = request.POST['recipient']
        content = request.POST['content']

        # Check if recipient exists in the database
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            # Handle case where recipient does not exist
            django_messages.error(
                request, f'User with username {recipient_username} does not exist.')
            return redirect('send_message')

        # Create new Message object
        message = Message(sender=request.user,
                          recipient=recipient, content=content)
        message.save()

        # Redirect to success page or show success message
        django_messages.success(request, 'Message sent successfully!')
        return redirect('messages')
    return render(request, 'send_message.html')

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
def add_like(request, post_id, user_id):
  like_list = []
  idx = 0
  for x in Like.objects.filter(post_id=post_id):
    like_list.append(Like.objects.filter(post_id=post_id).values("user_id")[idx]['user_id'])
    idx += 1

  if user_id in like_list:
    Like.objects.filter(post_id=post_id, user_id=user_id).delete()
  else:
    new_like = Like()
    new_like.post_id = post_id
    new_like.user_id = user_id
    new_like.save()

  return redirect('home')

def add_like_detail(request, post_id, user_id):
  like_list = []
  idx = 0
  for x in Like.objects.filter(post_id=post_id):
    like_list.append(Like.objects.filter(post_id=post_id).values("user_id")[idx]['user_id'])
    idx += 1

  if user_id in like_list:
    Like.objects.filter(post_id=post_id, user_id=user_id).delete()
  else:
    new_like = Like()
    new_like.post_id = post_id
    new_like.user_id = user_id
    new_like.save()

  return redirect('detail', post_id=post_id)

def likes_detail(request, post_id):
  post = Post.objects.get(id=post_id)

  return render(request, 'likes/detail.html', { 'post': post })


def username_update(request, user_id):
  return render(request, 'main_app/username_form.html')

def username_updated(request, user_id):
  this_user = User.objects.get(id=user_id)
  this_user.username = request.POST['username']
  for user in User.objects.values():
    if user['username'] == request.POST['username']:
      return redirect('username_update', user_id=user_id)
  this_user.save()
  return redirect('profile', user_id=user_id)


def bio_update(request, user_id):
  return render(request, 'main_app/bio_form.html')

def bio_updated(request, user_id):
  if not UserDescription.objects.filter(user_id=user_id).exists():
      this_user = UserDescription(description=request.POST['description'], user_id=user_id)
      this_user.save()
      return redirect('profile', user_id=user_id)
  else:
    this_user = UserDescription.objects.get(user_id=user_id)
    this_user.description = request.POST['description']
    this_user.save()
    return redirect('profile', user_id=user_id)

def user_photo_update(request, user_id):
  pass