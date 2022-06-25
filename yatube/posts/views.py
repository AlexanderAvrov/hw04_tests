from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import get_ten_posts_per_page


def index(request):
    """Вью-функция главной страницы"""
    template = 'posts/index.html'
    post_list = Post.objects.select_related('group', 'author')
    context = {
        'page_obj': get_ten_posts_per_page(request, post_list),
    }

    return render(request, template, context)


def group_posts(request, slug):
    """Вью-функция страниц сообществ"""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('group', 'author')
    context = {
        'group': group,
        'page_obj': get_ten_posts_per_page(request, post_list),
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Вью-функция просмотра профиля пользователя с публикациями"""
    author = get_object_or_404(
        User.objects.select_related(),
        username=username,
    )
    post_list = author.posts.all()
    context = {
        'page_obj': get_ten_posts_per_page(request, post_list),
        'author': author,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Вью-функция просмотра отдельной публикации"""
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Вью-функция страницы создания публикации"""
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()

        return redirect('posts:profile', username=post.author)

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """Вью-функция изменения публикации"""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()

        return redirect('posts:post_detail', post_id=post_id)

    return render(
        request,
        'posts/create_post.html',
        {'is_edit': True, 'form': form, 'post': post},
    )
