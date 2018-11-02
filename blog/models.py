# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     blog/models.py
   Description :
   Author :       JWang
   date：          2018/10/24
-------------------------------------------------
   Change Activity:
                   2018/10/24:
-------------------------------------------------
"""
__author__ = 'JWang'

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# 如果想继承user
#             new_user = user_form.save(commit=False)
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             profile = Profile.objects.create(user=new_user)
"""
class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='static/image/%Y/%m', default='static/image/default.jpg', max_length=200,
                              blank=True, null=True, verbose_name='用户头像')
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username
"""


class Tag(models.Model):
    """
    文章标签
    tag of posts
    """
    tag_name = models.CharField(u'标签名', max_length=100)

    def __str__(self):
        return self.tag_name


class Category(models.Model):
    """
    文章类型
    tag of posts
    """
    category_name = models.CharField(u'文章类型', max_length=100)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    # 内容相关
    title = models.CharField(max_length=200)  # 博客标题
    body = models.TextField(blank=True, null=True)  # 文章正文
    digest = models.TextField(blank=True, null=True)  # 文章摘要
    picture = models.CharField(max_length=200)  # 标题图片地址
    # 时间相关
    created_time = models.DateTimeField(auto_now_add=True)  # 文章的创建时间
    modified_time = models.DateTimeField()  # 文章最后修改时间
    # 其他人阅读评论
    view_num = models.BigIntegerField(default=0)  # 阅读数
    comment_num = models.BigIntegerField(default=0)  # 评论数
    # 外键
    author = models.ForeignKey(User, verbose_name=u'作者', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name=u'文章类型', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)  # 标签

    def __str__(self):
        return "文章: " + self.title + "\n作者：" + self.author.__str__()

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'post_id': self.id})

    def viewed(self):
        self.view_num += 1
        self.save(update_fields=['view_num'])

class Comment(models.Model):
    # 内容相关
    body = models.CharField(verbose_name='内容', max_length=300)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # 外键相关
    post = models.ForeignKey(Post, verbose_name='博客', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论', on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name=u'作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.body[:10]
