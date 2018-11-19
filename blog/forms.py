# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# 注册
class RegisterForm(forms.Form):
    error_msg = {
        'username': {'required': '用户名不能为空', 'max_length': '最大20', 'min_length': '用户名长度至少6'},
        'password': {'required': '用户名密码不能为空', 'max_length': '最大20', 'min_length': '密码长度至少6'},
    }
    username = forms.CharField(label='用户名', min_length=6, max_length=20, required=True,
                               error_messages=error_msg['username'])
    password = forms.CharField(label='密码', min_length=6, max_length=20, required=True,
                               validators=[
                                   RegexValidator(r'((?=.*\d))^.{6,20}$', '密码必须包含数字'),
                                   RegexValidator(r'((?=.*[a-zA-Z]))^.{6,20}$', '密码必须包含字母'),
                                   RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,20}$', '密码必须包含特殊字符'),
                                   RegexValidator(r'^.(\S){6,20}$', '密码不能包含空白字符'),
                               ],  # 用于对密码的正则验证
                               error_messages=error_msg['password'], widget=forms.PasswordInput)
    password_again = forms.CharField(label='确认密码', min_length=6, max_length=20, required=True,
                                     error_messages={'required': '密码不能为空!'}, widget=forms.PasswordInput)

    email = forms.EmailField(
        label='邮箱',
        required=True,
        min_length=6,
        max_length=30,
        error_messages={'required': '邮箱不能为空',
                        'invalid': '请输入正确的邮箱格式'},
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = User.objects.filter(username=username)
        print(username)
        if users:
            raise forms.ValidationError("用户名已经存在")
        return username

    def clean_email(self):
        # 对email的扩展验证，查找用户是否已经存在
        email = self.cleaned_data.get('email')
        email_count = User.objects.filter(email=email).count()  # 从数据库中查找是否用户已经存在
        if email_count:
            raise forms.ValidationError('该邮箱已经注册！')
        return email

    def clean__password_again(self):  # 查看两次密码是否一致
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_again')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('两次密码不匹配！')


# 登录
class LoginForm(forms.Form):
    error_msg = {
        'username': {'required': '用户名不能为空', 'max_length': '最大20', 'min_length': '至少6'},
        'password': {'required': '用户名密码不能为空', 'max_length': '最大20', 'min_length': '至少6'},
    }
    username = forms.CharField(label='用户名', min_length=6, max_length=20, required=True,
                               error_messages=error_msg['username'])
    password = forms.CharField(label='密码', min_length=6, max_length=20, required=True,
                               error_messages=error_msg['password'], widget=forms.PasswordInput)
