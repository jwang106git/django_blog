from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from blog.models import User
from blog.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO


# Create your views here.
class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register2.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        # 2. 验证
        print('errors1', form.errors)
        if form.is_valid():
            new_user = form.clean()
            del new_user['password_again']
            print(new_user)
            new_user = User.objects.create_user(**new_user)
            print(new_user)
            # new_user.set_password(form.cleaned_data['password'])
            print(request.META['HTTP_REFERER'])
            return redirect(reverse('auth:login'))
        print(form.errors)
        return render(request, 'register2.html', {'form': form})


def verify_code(request, *args):
    # 1，定义变量，用于画面的背景色、宽、高
    # random.randrange(20, 100)意思是在20到100之间随机找一个数
    bgcolor = tuple([random.randrange(20, 100), random.randrange(20, 100), 255])
    width = 100
    height = 25
    # 2，创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 3，创建画笔对象
    draw = ImageDraw.Draw(im)
    # 4，调用画笔的point()函数绘制噪点，防止攻击
    for i in range(0, 100):
        # 噪点绘制的范围
        xy = (random.randrange(0, width), random.randrange(0, height))
        # 噪点的随机颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制出噪点
        draw.point(xy, fill=fill)
    # 5，定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 6，随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 7，构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    # font = ImageFont.truetype('FreeMono.ttf', 23)
    font = ImageFont.truetype("static/fonts/Avenir.ttc", 23, index=1)
    # 8，构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 9，绘制4个字
    draw.text((5, 0), rand_str[0], font=font, fill=fontcolor)
    draw.text((27, 0), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 0), rand_str[2], font=font, fill=fontcolor)
    draw.text((72, 0), rand_str[3], font=font, fill=fontcolor)
    # 9，用完画笔，释放画笔
    del draw
    # 10，存入session，用于做进一步验证
    request.session['verifycode'] = rand_str

    # 11，内存文件操作
    buf = BytesIO()
    # 12，将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 13，将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# ajax登录校验回调视图函数
def login_ajax_check(request):
    # 1. 获取post内容
    print('login')
    username = request.POST.get("username")
    password = request.POST.get("password")
    vcode = request.POST.get('vcode')
    vcode_session = request.session.get('verifycode')
    url_before = request.POST.get("url_before")

    # 2. 验证
    if vcode != vcode_session:
        return JsonResponse({'msg': 'fail_verify'})
    else:
        user = authenticate(username=username, password=password)
        if user:
            # 这个就是使用auth组件的登录
            if user.is_active:  # 判断用户是否被激活
                login(request, user)
                # 如果调用login方法以后，
                # request对象就会激活user属性，这个属性不管登录或者未登录都是存在
                print(url_before)
                url_before = reverse('blog:index') if 'auth' in url_before else url_before
                return JsonResponse({'msg': 'ok', 'url': url_before})
            else:
                return JsonResponse({'msg': 'user_not_active'})
        else:
            return JsonResponse({'msg': 'fail_user'})


# ajax注册校验回调视图函数
def sign_up_ajax_check(request):
    # 1. 获取post内容
    print('sign up')
    print(request.POST)
    vcode = request.POST.get('vcode')
    vcode_session = request.session.get('verifycode')
    # url_before = request.POST.get("url_before")
    form = RegisterForm(request.POST, request.FILES)
    # 2. 验证
    if vcode != vcode_session:
        return JsonResponse({'msg': 'fail_verify', 'error': {'verify_code':'验证码错误'}})
    else:
        if form.is_valid():
            new_user = form.clean()
            del new_user['password_again']
            print(new_user)
            new_user = User.objects.create_user(**new_user)
            print(new_user)
            # new_user.set_password(form.cleaned_data['password'])
            print(request.META['HTTP_REFERER'])
            # return redirect(reverse('auth:login'))
            return JsonResponse({'msg': 'ok', 'url': reverse('auth:login')})
        else:
            print('form.errors')
            print(form.errors)
            return JsonResponse({'msg': 'error', 'error': form.errors})


class AuthLogin(View):
    """ 通过auth登录 """

    def get(self, request, *args):
        request.META['HTTP_REFERER'] = request.META.get('HTTP_REFERER', "/")
        form = LoginForm
        url_before = args[0] if len(args) > 0 else request.META['HTTP_REFERER']
        return render(request, 'login.html', {'form': form, 'url_before': url_before})


class AuthLogout(View):
    def get(self, request):
        url_before = request.META['HTTP_REFERER']
        url_before = "" if not url_before else url_before
        logout(request)  # 会清除 cookie,seesion
        return redirect(url_before)
