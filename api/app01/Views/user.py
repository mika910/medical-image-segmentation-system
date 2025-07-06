import os
import uuid

from django.shortcuts import render
import json
import re
import time
from django.shortcuts import render,redirect,HttpResponse
from django.core.exceptions import ValidationError
from django.http import JsonResponse,FileResponse
from rest_framework.views import APIView
from app01 import models
from app01.myTools import user_jwt, timetz
from app01.myTools.response import response
from app01.myTools.user_jwt import GenToken, ParseToekn

path = "file/userInfoImg"
os.makedirs(path, exist_ok=True)


'''用户操作'''
#登录
class Login_Api(APIView):
    def post(self,request):
        username = request.data.get("username","")
        password = request.data.get("password","")
        if username == "":
            return  response(503,"请输入用户名",None)
        if password == "":
            return  response(503,"请输入密码",None)

        try:
            datas = models.UserModel.objects.filter(username=username)
        except AttributeError:
            # 处理objects属性不存在的情况
            return response(503, "数据库访问错误", None)
        if datas.exists():
            user = datas.values()[0]
            if user['password'] != password:
                return response(503, "用户名或密码错误", None)

            token=GenToken(user["username"],user["uid"],user["level"])
            result = {
                "username": user["username"],
                "name":user["name"],
                "level": user["level"],
                "token": token,
            }
            return response(200,"登录成功",result)

        else:
            return  response(503,"用户名或密码错误",None)

        pass
#注册
# 在 Register 类中添加异常处理
class Register(APIView):
    def post(self,request):
        username = request.data.get('username', "")
        password = request.data.get('password', "")

        # 检测内容是否符合规则
        if username == "":
            data = {'code': 503, "msg": "请输入账号", 'data': ""}
            return JsonResponse(data)
        if password == "":
            data = {'code': 503, "msg": "请输入密码", 'data': ""}
            return JsonResponse(data)
        if len(password) < 6:
            data = {'code': 503, "msg": "用户密码最少长度为6位", 'data': ""}
            return JsonResponse(data)

        # 设置账号等级为普通用户
        level = 1
        # 检测账号是否已存在
        try:
            ex = models.UserModel.objects.filter(username=username)
            if ex.exists():
                data = {'code': 503, "msg": "账号已存在", 'data': ""}
                return JsonResponse(data)
        except AttributeError:
            # 处理objects属性不存在的情况
            data = {'code': 503, "msg": "数据库访问错误", 'data': ""}
            return JsonResponse(data)

        # 保存到数据库
        dic = {
            "uid": str(uuid.uuid4()),
            "username": username,
            "password": password,
            "level": level,
        }
        try:
            models.UserModel.objects.create(**dic)
        except Exception as e:
            data = {'code': 503, "msg": "注册失败", 'data': str(e)}
            return JsonResponse(data)
        data = {'code': 200, "msg": "注册成功 请登录", 'data': ""}
        return JsonResponse(data)


#用户个人信息获取和修改
class UserInfo(APIView):
    def get(self, request):
        '''用户个人信息获取'''
        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)

        obj = models.UserModel.objects.filter(username=token_dic['data']['username'])
        if obj.exists():
            data = obj.values()
            data = [i for i in data]
            data = data[0]
            data['password'] = ""
            data['CreatedAt'] = data['CreatedAt'].astimezone(timetz.shanghai_tz).strftime("%Y-%m-%d")
            return response(200, "查询成功", data)

        else:
            return response(401, "用户信息不存在", None)

    def put(self, request):
        '''用户个人信息修改'''

        name = request.data.get("name", "")
        password = request.data.get("password")
        phone = request.data.get("phone", "")


        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)
        try:
            obj = models.UserModel.objects.get(username=token_dic['data']['username'])
        except Exception as e:
            return response(401, "用户信息不存在", None)
        if password:
            if len(password) < 6:
                return response(503, "密码长度最少为6位", None)
            if len(password) > 32:
                return response(503, "密码长度最长为32位", None)
            obj.password = password
        obj.phone = phone
        obj.name = name
        obj.save()
        return response(200, "修改成功", None)


#用户头像获取和修改
class UserInfoImg(APIView):
    def get(self,request):
        # 用户头像获取
        img =request.query_params.get("img")
        file_path = path+"/"+img

        if not os.path.exists(file_path):
            return response(503, "文件不存在", None)

        f = open(file_path, 'rb')
        r = FileResponse(f, as_attachment=False, filename=f"{img}")
        return r


    def post(self, request):
        # 上传用户图片
        # 上传
        file_obj = request.FILES.get('file')
        # id
        file_uuid = str(uuid.uuid4())
        file_type = file_obj.name.split(".")[-1]
        # 上传人
        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)
        username = token_dic['data']['username']
        file_uuid = file_uuid+ f".{file_type}"
        # 文件大小
        with open(f"{path}/{file_uuid}", "wb") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        try:
            obj=models.UserModel.objects.get(username=username)
        except Exception as e:
            return response(403, "用户信息不存在", None)
        obj.img = file_uuid
        obj.save()
        return response(200, "上传成功", file_uuid)


# 在现有代码中添加以下类

class VerifyIdentity(APIView):
    def post(self, request):
        '''验证用户身份'''
        username = request.data.get("username", "")
        phone = request.data.get("phone", "")
        
        if username == "":
            return response(503, "请输入用户名", None)
        if phone == "":
            return response(503, "请输入手机号", None)
        
        # 查询用户是否存在
        try:
            user = models.UserModel.objects.filter(username=username)
            if not user.exists():
                return response(503, "用户不存在", None)
            
            # 验证手机号是否匹配
            user_data = user.values()[0]
            if user_data['phone'] != phone or not phone:
                return response(503, "手机号不匹配", None)
        except AttributeError:
            # 处理objects属性不存在的情况
            return response(503, "数据库访问错误", None)
        
        return response(200, "身份验证成功", None)

class ResetPassword(APIView):
    def post(self, request):
        '''重置密码'''
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        
        if username == "":
            return response(503, "请输入用户名", None)
        if password == "":
            return response(503, "请输入新密码", None)
        
        # 验证密码长度
        if len(password) < 6:
            return response(503, "密码长度最少为6位", None)
        if len(password) > 32:
            return response(503, "密码长度最长为32位", None)
        
        # 查询用户是否存在
        try:
            user = models.UserModel.objects.get(username=username)
        except models.UserModel.DoesNotExist:
            return response(503, "用户不存在", None)
        except AttributeError:
            # 处理objects属性不存在的情况
            return response(503, "数据库访问错误", None)
        except Exception as e:
            return response(503, f"查询用户时出错: {str(e)}", None)
        
        # 更新密码
        try:
            user.password = password
            user.save()
        except Exception as e:
            return response(503, f"更新密码时出错: {str(e)}", None)
        
        return response(200, "密码重置成功", None)
