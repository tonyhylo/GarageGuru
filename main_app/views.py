from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
  return render(request, 'home.html')

def messages(request):
  return render(request, 'messages.html')

def profile(request):
  return render(request, 'profile.html')