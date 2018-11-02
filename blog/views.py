from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, render_to_response
from .models import Post, Comment
from django.views import View
from django.urls import reverse
from django.views.decorators.cache import cache_page
import time
from django.views.generic.detail import DetailView
from django.core.cache import cache


# Create your views here.
class Detail(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.view_num = post.view_num + 1
        post.save()
        comment_list = Comment.objects.filter(post=post)
        return render(request, 'blog/detail.html', context={'post': post, 'comment_list': comment_list})


# 另一种方法，使用detail view
class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    pk_url_kwarg = 'post_id'
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super(PostDetailView, self).get_object()
        obj.viewed()
        self.object = obj
        return obj

    def get_context_data(self, **kwargs):
        postid = int(self.kwargs[self.pk_url_kwarg])
        comment_list = Comment.objects.filter(post_id=postid)
        kwargs['comment_list'] = comment_list

        return super(PostDetailView, self).get_context_data(**kwargs)


def aside():
    post_list_newest = Post.objects.all().order_by('-created_time')
    return post_list_newest[0:3]


@cache_page(24 * 3600)
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    post_list_newest = aside()
    return render_to_response('blog/index.html', context={
        'post_list': post_list,
        'title': '我的博客首页',
        'post_list_newest': post_list_newest,
    })


def submit_comment(request):
    if request.method == 'POST':
        temp_user = request.user
        temp_body = request.POST.get('comment_body')
        post_id = request.POST.get('post_id')
        if temp_body and 2 < len(temp_body) < 550:
            print(temp_user, temp_body, post_id)
            if temp_user and post_id:
                new_comment = Comment.objects.create(body=temp_body, user=temp_user, post_id=post_id)
                new_comment.save()
                post = Post.objects.filter(id=post_id)[0]
                post.comment_num = post.comment_num + 1
                post.save()
                return redirect(reverse('blog:detail', kwargs={'post_id': post_id}))
        if not temp_body:
            print('not temp')
        else:
            print(len(temp_body))
        return HttpResponse('wrong request')


def recommend():
    post_list = Post.objects.all().order_by('view_num')
    return post_list[0:3]


@cache_page(48 * 3600)
def page_not_found(request):
    post_list = recommend()
    return render_to_response('errors/404.html', context={'post_list': post_list})


@cache_page(48 * 3600)
def page_error(request):
    post_list = recommend()
    return render_to_response('errors/500.html', context={'post_list': post_list})


class Search(View):
    def post(self, request):
        title = request.POST.get('title', 'django')
        error_msg = ''
        post_list = None

        if not title:
            error_msg = '请输入关键词'
        else:
            post_list = Post.objects.filter(title__icontains=title)

        return render(request, 'blog/index.html', {'error_msg': error_msg,
                                                   'post_list': post_list})


def view_post(post_id):
    post = get_object_or_404(Post, id=post_id)
    post.view_num = post.view_num + 1
    post.save()
    num_list = [post.view_num, post.comment_num]
    return num_list


def get_time():
    return time.time()
