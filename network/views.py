from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from .models import Post

# Create your views here.
def index(request):
    return render(request, "network/index.html")

@login_required
def post(request):
    if request.method=="POST":
        new_post = request.POST.get("post-input")
        Post.objects.create(
            content=new_post,
            author= request.user
        )
        messages.success(request, 'Post created')
        return redirect('index')
    return redirect('index')

@login_required
def create_post(request):
    if request.method == "POST":
        new_post = request.POST.get("post-input")
        Post.objects.create(
            content=new_post,
            author = request.user
        )
        messages.success(request, 'Post created')
        return redirect('index')
    return render(request, 'network/create_post.html')