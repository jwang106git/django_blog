from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, render_to_response
from .models import Post, Comment
from django.views import View
from django.urls import reverse
from django.views.decorators.cache import cache_page
import time
from django.views.generic.detail import DetailView
from django.core.cache import cache
from django.utils.safestring import mark_safe
import markdown


# Create your views here.
class Detail(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.view_num = post.view_num + 1
        post.save()
        comment_list = Comment.objects.filter(post=post)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
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


def pagenation(request, current_url, post_list_length=6, model_name=Post, get_condition=None):
    if request.method == 'GET':
        # post per page
        post_per_page = int(request.COOKIES.get('post_per_page', 3))
        print('post_per_page is ', post_per_page)
        if post_per_page not in [3, 10, 50, 100]:
            post_per_page = 3
        print('post_per_page is ', post_per_page)
        # url list
        page_index_list = []
        count, remain = divmod(post_list_length, post_per_page)
        max_page_num = count + 1 if remain > 0 else count

        # page_num
        page_num = int(request.GET.get('p', 1))
        page_num = page_num if page_num > 1 else 1
        page_num = page_num if page_num <= max_page_num else max_page_num

        # post_list
        post_start = (page_num - 1) * post_per_page
        post_end = page_num * post_per_page
        if get_condition:
            post_list = model_name.objects.filter(get_condition)[post_start, post_end]
        else:
            post_list = model_name.objects.all().order_by('-created_time')
            post_list = post_list[post_start: post_end]
        # page_index_list，也就是所有页的index
        start_page_num = page_num - 4 if page_num >= 4 else 0
        end_page_num = page_num + 3 if page_num <= (max_page_num - 3) else max_page_num

        for page_i in range(start_page_num, end_page_num):
            temp = "<li><a href='%s?p=%s'>%s</a></li>" % (current_url, page_i + 1, page_i + 1)
            if page_i + 1 == page_num:
                temp = "<li class='active'><a href='%s?p=%s'>%s<span class='sr-only'>(current)</span></a></li>" % (
                    current_url, page_i + 1, page_i + 1)
            page_index_list.append(temp)

        # url list--> str --> mark_safe
        page_index = ' '.join(page_index_list)
        page_index = mark_safe(page_index)

        # 上一页和下一页的class
        last_page_class = ''
        next_page_class = ''

        # 上一页和下一页的index
        last_page_href = '%s?p=%s' % (current_url, page_num - 1)
        next_page_href = '%s?p=%s' % (current_url, page_num + 1)
        if page_num == 1:
            last_page_href = '%s?p=%s' % (current_url, 1)
            last_page_class = 'disabled'
        if page_num == max_page_num:
            next_page_href = '%s?p=%s' % (current_url, page_num)
            next_page_class = 'disabled'

        # return
        return page_index, post_list, last_page_href, next_page_href, last_page_class, next_page_class, max_page_num


def index(request):
    post_list_newest = aside()
    current_url = reverse('blog:index')
    post_list_length = len(Post.objects.all())

    page_index, post_list, last_page_href, next_page_href, last_page_class, next_page_class, max_page_num = \
        pagenation(request, current_url, post_list_length)
    return render(request, 'blog/index.html', context={
        'post_list': post_list,
        'page_index': page_index,
        'title': '我的博客首页',
        'post_list_newest': post_list_newest,
        'last_page_href': last_page_href,
        'next_page_href': next_page_href, 'last_page_class': last_page_class,
        'next_page_class': next_page_class, 'max_page_num': max_page_num
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
        print('post', request.POST)
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
