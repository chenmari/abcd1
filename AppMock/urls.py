from django.contrib import admin
from django.urls import path,re_path
from Myapp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('project_list/',project_list),  #对应后端函数
    re_path('del_project/(?P<pid>.+)/',del_project),#删除项目
    path('',project_list),# 进入首页项目列表
    path('add_project/', add_project),  # 增加新的项目
    path('login/',login),# 进入登录页面
    path('accounts/login/',login),# 当忘记带登录态的时候访问的登录页
    ########
    path('sign_in/',sign_in),# 登录
    path('sign_up/',sign_up), #注册
    path('logout/',logout),# 退出

    path('reset_password/',reset_password),
    path('send_email_pwd/',send_email_pwd),

    re_path('mock_list/(?P<project_id>.+)/',mock_list),
    #新增mock单元url
    re_path('add_mock/(?P<project_id>.+)/',add_mock),
    re_path('del_mock/(?P<mock_id>.+)/', del_mock),
]
