from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm


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


def add_comment(request, post_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.post_id = post_id
    new_comment.save()
  return redirect('detail', post_id=post_id)


def delete_comment(request, post_id, comment_id):
  comment = Comment.objects.get(id=comment_id)
  comment.delete()
  return redirect('detail', post_id=post_id)


