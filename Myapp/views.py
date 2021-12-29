from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from Myapp.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
# 进入项目列表
@login_required()
def project_list(request):
    buttons = [{"name":"新增项目","href":"/add_project/","icon":"folder"},
               {"name":"项目数据","href":"/1234/","icon":"folder"}]
    page_name = "项目详情页面"
    project_qs = DB_project.objects.all()
    return render(request,'project_list.html',{"projects":project_qs,"buttons":buttons,"page_name":page_name})

# 删除项目
def del_project(request,pid):
    DB_project.objects.filter(id=pid).delete()
    return HttpResponseRedirect('/project_list/')

# 增加项目
def add_project(request):
    DB_project.objects.create(name='新项目',creater=request.user.username)
    return HttpResponseRedirect('/project_list/')

# 进入登录页面
def login(request):
    return render(request,'login2.html')  #返回登录页面


# 登录
def sign_in(request):
    # 获取来自页面用户输入的用户名和密码
    a = request.GET['in_username']
    b = request.GET['in_password']
    # 去数据库用户表中查询真假
    user = auth.authenticate(username=a,password=b)
    # 如果为假，不进行登录，重新返回登录页面
    if user is None:
        # return HttpResponse('密码错误')
        return HttpResponseRedirect('/login/')
     # 如果为真，登录，跳转到项目列表页
    else:
        auth.login(request,user)
        request.session['user'] = a
        return HttpResponseRedirect('/project_list/')

# 退出登录
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

# 注册
def sign_up(request):
    # 获取用户名 密码 邮箱
    a = request.GET['up_username']
    b = request.GET['up_password']
    c = request.GET['up_email']
    # 注册
    try:# 注册成功
        user = User.objects.create_user(username=a,email=c,password=b)
        user.save()
        auth.login(request,user)
        request.session['user'] = a
        return HttpResponseRedirect('/project_list/')
    except:
        # 注册失败
        return HttpResponseRedirect('/login/')

# 重设密码
def reset_password(request):
    # 获取用户名，验证码，新的密码
    username = request.GET['fg_username']
    code = request.GET['fg_code']
    password = request.GET['fg_password']
    # 判断验证码
    if code == User.objects.filter(username=username)[0].last_name:
        User.objects.filter(username=username).update(password=make_password(password))
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponse('code is wrong!')

# 发送验证码邮件
def send_email_pwd(request):
    # 获取登录用户名
    username = request.GET['username']
    # 根据用户名去用户表找到邮箱
    email = User.objects.filter(username=username)[0].email
    # 生成随机验证码
    code = str(random.randint(1000,9999))
    print(code)
    # 保存验证码
    User.objects.filter(username=username).update(last_name=code)

    # 发送邮件
    msg = '这是需要找回密码的验证码：'+code
    send_mail('mock平台找回密码功能',msg,settings.EMAIL_FROM,[email])
    print(msg)
    # 返回yes
    return HttpResponse('yes')


#进入mock的列表详情页
def mock_list(request,project_id):
    #从数据库中取出符合的mock列表
    mocks_a = DB_mock.objects.filter(project_id = project_id)

    project = DB_project.objects.filter(id=project_id)[0]
    res = {}
    res['mocks'] = mocks_a
    res['buttons'] = [{"name": "新增单元", "href": "/add_mock/%s/"%project.id, "icon": "folder"},
               {"name": "抓包导入", "href": "", "icon": "folder"},
               {"name": "项目设置", "href": "", "icon": "folder"},
               {"name": "启动服务", "href": "", "icon": "folder"},
               {"name": "关闭服务", "href": "", "icon": "folder"},
               ]
    res['page_name'] = "项目详情页:【%s】"%project.name
    return render(request,'mock_list.html',res)


#新增mock单元项目
def add_mock(request,project_id):
    DB_mock.objects.create(name="新mock单元",project_id=project_id)
    return HttpResponseRedirect('/mock_list/%s/'%project_id)

#删除mock单元
def del_mock(request,mock_id):
    mocks = DB_mock.objects.filter(id=mock_id)
    project_id = mocks[0].project_id
    mocks.delete()
    return HttpResponseRedirect('/mock_list/%s/'%project_id)
