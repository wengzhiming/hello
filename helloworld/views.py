from django.shortcuts import render
from django.http import HttpResponse
from helloworld.models import helloUser

from django.http import JsonResponse

from django.contrib import auth
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO


def index(request):
    return render(request, 'index.html')
# Create your views here.

def login_success(request):
    if request.method == 'POST':
        try:
            user = helloUser.objects.get(username=request.POST.get('username'))
            print(user)
            if user:
                if user.password == request.POST.get('password'):
                    if request.POST.get('verify_code_index') == request.session.get('verifycode'):
                        return HttpResponse('登录成功,HHHH')
                    else:
                        return render(request, 'index.html')
                else:
                    return HttpResponse('密码错误')
        except Exception as e:
                print(e)
                return HttpResponse('网络错误')


def registe(request):
    return render(request, 'registe.html')

def registe_loading(request):
    string_1 = ['账号重复请重新注册','密码为空，请重新输入']
    if request.method == 'POST':
        try:
                user = helloUser.objects.get(username=request.POST.get('username'))
                if request.POST.get('username') == user.username:
                    return render(request, 're_register.html')
        except:
                hellouser = helloUser()
                if request.POST.get('username')!='' or request.POST.get('password')!='':
                    hellouser.username = request.POST.get('username')
                    hellouser.password = request.POST.get('password')
                    hellouser.save()
                    return render(request,'registe_success.html')
                else:
                    return render(request,'re_register.html')
    else:
        return render(request,'404.html')



def verify_code(request):
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMYOU.TTF", 20)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    buf = BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')