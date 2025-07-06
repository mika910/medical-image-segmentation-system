import uuid
from django.http import JsonResponse,FileResponse
from rest_framework.views import APIView
from app01 import models
from app01.myTools.pageGet import pageGet
from app01.myTools.response import response
from app01.myTools.user_jwt import ParseToekn

# 数据集添加请求管理



class Datalist(APIView):

    #数据列表
    def get(self,request):
        page,pagesize =pageGet(request)
        #计算分页值
        start_page = page * pagesize -pagesize           #计算每一页显示内容的范围
        end_page = page * pagesize

        #提取搜索参数
        dic={}
        username=request.query_params.get("username","")
        title=request.query_params.get("title","")
        describe=request.query_params.get("describe","")
        source=request.query_params.get("source","")
        state=request.query_params.get("state","")
        admin_reply=request.query_params.get("admin_reply","")
        if username:
            dic['username__icontains'] =username
        if title:
            dic['title__icontains'] = title
        if describe:
            dic['describe__icontains'] = describe
        if source:
            dic['source__icontains'] = source
        if state:
            dic['state'] = state
        if admin_reply:
            dic['admin_reply__icontains'] = admin_reply

        #获取用户凭证
        token_dic ,err=  ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)

        #管理员可以看所有的
        if token_dic["data"]["level"] == 10:
            # 管理员可以看所有的
            pass
        else:
            # 用户只能看自己的
            dic['username'] = token_dic["data"]['username']





        datas = models.DataAddAskModel.objects.filter(**dic).order_by('-id')[start_page:end_page].values() #从数据库中提取数据
        datas = [i for i in datas]
        #查询总数据条数
        total = models.DataAddAskModel.objects.filter(**dic).count()

        return response(200,"查询成功",{
                "data":datas,
                "total":total
            })

    #填写新的表单
    def post(self,request):
        # 获取用户凭证
        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)

        #提取前端提交的json参数
        title = request.data.get('title',"")
        describe = request.data.get('describe',"")
        source = request.data.get('source',"")

        if title == "":
            data = {'code': 503, "msg": "请输入标题", 'data': ""}
            return JsonResponse(data)
        if source == "":
            data = {'code': 503, "msg": "请填写数据集来源", 'data': ""}
            return JsonResponse(data)


        # 保存到数据库
        # 将需要写入数据库的内容 构建为字典格式
        dic = {
            "username": token_dic["data"]["username"],
            "uid":token_dic["data"]["uid"],
            "title": title,
            "describe": describe,
            "source": source,
            "state": "等待管理员处理",
        }
        try:
            models.DataAddAskModel.objects.create(**dic)       #写入到数据库    传值时需要加**
        except Exception as e:
            data = {'code': 503, "msg": "提交数据失败", 'data': str(e)}
            return JsonResponse(data)

        data = {'code': 200, "msg": "提交成功", 'data': ""}
        return JsonResponse(data)

    #修改数据
    def put(self,request):
        #验证限权
        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)

        if token_dic["data"]["level"] != 10:
            data = {'code': 503, "msg": "限权不足", 'data': ""}
            return JsonResponse(data)



        #获取必填值
        id = request.data.get("id","")
        title = request.data.get("title","")
        describe = request.data.get("describe","")
        source =  request.data.get("source","")
        state = request.data.get("state","")
        admin_reply=  request.data.get("admin_reply","")


        if id == "":
            return response(503, "参数错误", None)




        data_obj = models.DataAddAskModel.objects.filter(id=id)
        if data_obj.exists():
            pass
        else:
            return response(503, "数据不存在", None)


        data_obj = models.DataAddAskModel.objects.get(id=id)


        #添加需要更新的字段
        data_obj.title=  title
        data_obj.describe = describe
        data_obj.source = source
        data_obj.state= state
        data_obj.admin_reply= admin_reply
        #进行更新操作
        data_obj.save()
        return response(200, "修改成功", None)

    #删除数据
    def delete(self,request):
        #验证限权
        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)
        if token_dic["data"]["level"] != 10:
            data = {'code': 503, "msg": "限权不足", 'data': ""}
            return JsonResponse(data)

        #提取出需要删除的数据id
        ids=request.query_params.get("id")
        if ids == "":
            data = {'code': 503,"msg":"需要删除的数据id为空", 'data':""}
            return JsonResponse(data)
        ids=[i for i in ids.split(",") if i]
        Obj=models.DataAddAskModel.objects.filter(id__in=ids)        #查询该id的数据是否存在
        count = Obj.count()
        if not Obj.exists():              #不存在的状态
            data = {'code': 503, "msg": "数据不存在", 'data': ""}
            return JsonResponse(data)
        Obj.delete()             #进行删除
        data = {'code': 200, "msg": f"成功删除了{count}条数据", 'data': ""}
        return JsonResponse(data)


#获取单条数据
class DataOne(APIView):
    def get(self,request):
        id = request.query_params.get("id","")
        if id == "":
            return response(503,"查询失败","参数错误")


        #获取用户凭证
        token_dic ,err=  ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)

        dic = {
            "id":id,
        }
        #管理员可以看所有的
        if token_dic["data"]["level"] == 10:
            # 管理员可以看所有的
            pass
        else:
            # 用户只能看自己的
            dic["username"] = token_dic["data"]['username']


        datas=models.DataAddAskModel.objects.filter(**dic).values()
        if len(datas) == 0:
            return response(503,"未查询到对应数据",None)

        return response(200, "查询成功", datas[0])