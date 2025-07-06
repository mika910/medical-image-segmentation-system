"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.Views import user, adminUser, detection, data_add_ask

urlpatterns = [
    path('api/user/login', user.Login_Api.as_view()),     #登录接口
    path('api/user/register', user.Register.as_view()),  #注册接口

    path('api/user/info', user.UserInfo.as_view()),       #用户个人信息接口
    path('api/user/img', user.UserInfoImg.as_view()),     #用户头像接口



    path('api/admin/user', adminUser.Admin_User_list.as_view()),  #获取用户列表
    path('api/admin/user/one', adminUser.Admin_User_one.as_view()), #用户用户具体信息


    path('api/detection', detection.Detection.as_view()),  # 进行检测
    path('api/detection/model', detection.dataFileList.as_view()),  #获取可用的模型和数据集文件
    path('api/detection/img', detection.FileApi.as_view()),  # 获取检测后的图片
    path('api/detection_list', detection.LIstApi.as_view()),  #获取检测历史


    path('api/data_add_ask_list', data_add_ask.Datalist.as_view()),  # 数据集添加请求管理
    path('api/data_add_ask_one', data_add_ask.DataOne.as_view()),  # 数据集添加请求管理


]
