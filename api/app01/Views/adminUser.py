import sys
import uuid
from django.shortcuts import render
import json
import re
import time
from django.shortcuts import render,redirect,HttpResponse
from django.core.exceptions import ValidationError
from django.http import JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt   #关闭post认证
from rest_framework.views import APIView
from app01 import models
from app01.myTools import user_jwt
from app01.myTools.pageGet import pageGet
from app01.myTools.response import response

'''管理员操作'''



def adminCreate():
    #创建初始管理员账号
    try:
        ex = models.UserModel.objects.filter(username="admin")
        if ex.exists():
            print("初始管理员账号已存在")
            return
    except Exception as e:
        return

    # 保存到数据库
    dic = {  # 将需要写入数据库的内容 构建为字典格式
        "uid": str(uuid.uuid4()),
        "username": "admin",
        "password": "admin",
        "name": "主管理员",
        "phone": "",
        "level": 10,
    }
    try:
        models.UserModel.objects.create(**dic)  # 写入到数据库    传值时需要加**
    except Exception as e:
        print("创建管理员账号失败",e)
        sys.exit()

adminCreate()



class Admin_User_list(APIView):
    def get(self,request):
        '''用户列表获取'''
        page,pagesize =pageGet(request)
        #计算分页值
        start_page = page * pagesize -pagesize           #计算每一页显示内容的范围
        end_page = page * pagesize

        dic={}
        username=request.query_params.get("username","")
        name=request.query_params.get("name","")
        phone=request.query_params.get("phone","")

        if username:
            dic['username__icontains'] =username
        if name:
            dic['name__icontains'] = name
        if phone:
            dic['phone__icontains'] = phone


        datas = models.UserModel.objects.filter(**dic).order_by('-id')[start_page:end_page].values() #从数据库中提取数据
        datas = [i for i in datas]
        #查询总数据条数
        total = models.UserModel.objects.filter(**dic).count()

        return response(200,"查询成功",{
                "data":datas,
                "total":total
            })


    def post(self,request):
        '''添加用户'''
         #提取前端提交的json参数
        username = request.data.get('username',"")
        password = request.data.get('password',"")
        name = request.data.get('name',"")
        phone = request.data.get('phone',"")
        level = request.data.get('level',"")

        if username == "":
            data = {'code': 503, "msg": "请输入账号", 'data': ""}
            return JsonResponse(data)
        if password == "":
            data = {'code': 503, "msg": "请输入密码", 'data': ""}
            return JsonResponse(data)
        if len(password) < 6:
            data = {'code': 503, "msg": "用户密码最少长度为6位", 'data': ""}
            return JsonResponse(data)
        if name == "":
            data = {'code': 503, "msg": "请填写账号昵称", 'data': ""}
            return JsonResponse(data)


        #如果没有选择等级 默认为普通用户
        if level == "":
            level = 0

        #检测账号是否已存在
        ex=models.UserModel.objects.filter(username=username)
        if ex.exists():
            data = {'code': 503, "msg": "账号已存在", 'data': ""}
            return JsonResponse(data)

        # 保存到数据库
        dic = {  # 将需要写入数据库的内容 构建为字典格式
            "uid":str( uuid.uuid4()),
            "username": username,
            "password":password,
            "name": name,
            "phone": phone,
            "level": level,
        }
        try:
            models.UserModel.objects.create(**dic)       #写入到数据库    传值时需要加**
        except Exception as e:
            data = {'code': 503, "msg": "新建用户失败", 'data': str(e)}
            return JsonResponse(data)

        data = {'code': 200, "msg": "新建用户成功", 'data': ""}
        return JsonResponse(data)
    def put(self,request):
        '''修改用户'''
        #获取必填值
        uid = request.data.get("uid","")
        name = request.data.get("name","")
        password =  request.data.get("password","")
        phone = request.data.get("phone","")
        level= int(request.data.get("level", "0"))

        #验证是否填写
        if uid == "":
            return response(503, "参数错误", None)
        if name == "":
            data = {'code': 503, "msg": "请填写账号昵称", 'data': ""}
            return JsonResponse(data)


        data_obj = models.UserModel.objects.filter(uid=uid)
        if data_obj.exists():
            pass
        else:
            return response(503, "数据不存在", None)

        data_obj = models.UserModel.objects.get(uid=uid)
        #查看是否更改了密码
        if password != "":
            if len(password) < 6:
                data = {'code': 503, "msg": "用户密码最少长度为6位", 'data': ""}
                return JsonResponse(data)

            #更改了密码
            data_obj.password =password




        #添加需要更新的字段
        data_obj.name=  name
        data_obj.phone = phone
        data_obj.level = level
        #进行更新操作
        data_obj.save()
        return response(200, "修改成功", None)

    def delete(self,request):
        '''删除用户'''
        #提取出需要删除的用户id
        ids=request.query_params.get("id")
        if ids == "":
            data = {'code': 503,"msg":"需要删除的用户id为空", 'data':""}
            return JsonResponse(data)
        ids=[i for i in ids.split(",") if i]
        Obj=models.UserModel.objects.filter(id__in=ids)        #查询该id的数据是否存在
        count = Obj.count()
        if not Obj.exists():              #不存在的状态
            data = {'code': 503, "msg": "用户不存在", 'data': ""}
            return JsonResponse(data)
        Obj.delete()             #进行删除
        data = {'code': 200, "msg": f"成功删除了{count}条数据", 'data': ""}
        return JsonResponse(data)


#获取单条数据
class Admin_User_one(APIView):
    def get(self,request):
        uid = request.query_params.get("uid","")
        if uid == "":
            return response(503,"查询失败","参数错误")

        datas=models.UserModel.objects.filter(uid=uid).values()
        if len(datas) == 0:
            return response(503,"未查询到对应数据",None)

        return response(200, "查询成功", datas[0])