from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Like

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-date')
    posts, liked_posts = create_posts(request, posts)
    return render(request, "network/index.html", {
        'posts': posts,
        'liked_posts': liked_posts
    })

def create_posts(request, posts):
    """
    Helper funcion to paginate posts and get liked posts by user
    """
    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    if request.user.is_authenticated:
        # get the ID's of posts that are liked on the current page
        liked_posts = Like.objects.filter(liked_by= request.user, liked_post__in=posts).values_list('liked_post_id', flat=True)
    else:
        liked_posts = []
    return posts, liked_posts


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