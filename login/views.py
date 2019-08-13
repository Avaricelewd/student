from django.shortcuts import render,redirect
from .models import User
import hashlib
from django.http import HttpResponse
import random
import string
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from static import jpg
# Create your views here.

def index(request):
    # 假设 服务端判断 request.cookie['session_id'],session_id没有或不正确禁止登录
    return render(request, 'login/index.html', context={})


def register(request):
    """GET 返回注册表单"""
    if request.method == 'GET':
        return render(request, 'login/register.html', context={})
    elif request.method == 'POST':
        context = {}
        name = request.POST['name']
        password = request.POST['password']
        # 密码加密  # 也可以from django.contrib.auth.hashers import make_password ,check_password
        md5 = hashlib.md5()
        md5.update(password.encode())
        hash_password = md5.hexdigest()

        if len(name) < 8:
            context['error_message'] = '用户名太短'
            return render(request, 'login/register.html', context)

        # return render(request, 'login/register.html', context)  # 失败
        user = User(name=name,password=password,hash_password = hash_password)
        user.save()
        return redirect(to='/login/index/') # 成功返回首页

def register_check(request):
    """检查注册参数，返回json结果
    :param 客户端的表单格式  name字段
    :method 请求方式 POST
    :return json格式发字符串

    {
        "code":100,      # 200成功
        "status":"falid",  # ok成功
        "error_message":""，  # 用户名太短 等错误信息
    },

    """
    import json
    resp_obj = {}
    name = request.POST['name']
    if len(name) <= 1:
        # 讲ajax时的反例
        resp_obj = {
            'code':100,
            'status':'验证失败',
            'error_message':'用户名太短',
        }
        resp_json = json.dumps(resp_obj)
        print(type(resp_obj))
        print(type(resp_json))
        return HttpResponse(resp_json)

def verify_image(request,width,height):
    words_count = 4   # 验证码中的字符长度
    width = int(width)  # 图片宽度
    height = int(height)  # 图片高度
    size = int(min(width / words_count , height) / 1.3)  # 字体大小
    bg_color = (random.randint(200,255),random.randint(200,255),random.randint(200,255))
    img = Image.new('RGB',(width,height),bg_color)  # 创建图像

    font = ImageFont.truetype('arial.ttf',size=size)  # 导入字体

    draw = ImageDraw.Draw(img)   # 创建画笔

    text = string.digits + string.ascii_letters   # 数字+大写字母
    verify_text = ''
    for i in range(words_count):
        text_color = (random.randint(0,160),random.randint(0,160),random.randint(0,160))  # 确定文字的颜色
        left = width * i / words_count + (width / 4 - size) /2  # i为第几个文字
        top = (height - size) /2

        word = text[random.randint(0,len(text) - 1 )]
        verify_text += word
        draw.text((left,top),word,font=font,fill=text_color)

    for i  in range(30):
        text_color = (255,255,255)  #白色的颜色
        left = random.randint(0,width)
        top = random.randint(0,height)
        draw.text((left,top),'*',font=font,fill=text_color)

    for i in range(5):
        line_color = (random.randint(0,160),random.randint(0,160),random.randint(0,160))
        line = (random.randint(0,width),random.randint(0,height),random.randint(0,width),random.randint(0,height))
        draw.line(line,fill=line_color)

    del draw

    image_stream = BytesIO
    img.save(image_stream,'jpeg')
    request.session['verify'] = verify_text
    return HttpResponse(image_stream.getvalue(),'image/jpeg')
















def do_register(request):
    pass

def login(request):
    if request.method == 'GET':
        return render(request,'login/login.html',context={})
    elif request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']

        context={}
        user_list = User.objects.filter(name=name,password=password) # 多个where条件逗号分隔，代表and 连接条件。
        if user_list:
            # 登录成功

            # user_list[0].name + time.now()  通过hash生成session_id
            # HttpResponse set_cookie {'session_id':'ssdvvss'}
            # 客户端接收到响应  根据set_cookie 响应头把数据存到自己的cookie中
            # 之后客户端每一次请求，都会带上cookie， 服务器就会比对是否存在，存在即用户已登录
            # django已经封装了方法，我们可以简单在响应头里设置cookie,下一个
            request.session['is_login'] = True
            request.session['user_name'] = user_list[0].name
            request.COOKIES['is_login'] = True
            request.COOKIES['user_name'] = user_list[0].name
            return redirect(to='/login/index/')
        else:
            # 登录失败
            if User.objects.filter(name=name).exists():
                context['message']= '密码错误'
                return render(request, 'login/login.html', context)
            else:
                context['message'] = '用户名不存在，请先注册'
                return render(request,'login/login.html',context)



def do_login(request):
    pass


def logout(request):
    pass



