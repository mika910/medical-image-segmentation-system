import os
import re
import uuid
from django.http import JsonResponse, FileResponse
from rest_framework.views import APIView
from app01 import models
from app01.model import visualizeINvue, vis_synapse, vis_acdc
from app01.myTools.pageGet import pageGet
from app01.myTools.response import response
from app01.myTools.timetz import shanghai_tz
from app01.myTools.user_jwt import ParseToekn
from urllib.parse import quote
import nibabel as nib

path = "file/img"
os.makedirs(path, exist_ok=True)




#检测后的图片获取
class FileApi(APIView):
    def get(self, request):
        # 图片获取显示
        try:
            mode = request.query_params.get("mode")
            mid = request.query_params.get("mid")
            # 检查需要的是不是为原图
            obj = models.DetectionModel.objects.filter(mid_handle=mid)
            if not obj.exists():
                return response(503, "图片不存在", "")

            data = obj.get()
            f = open(data.path_handle, 'rb')
            if mode:
                # 下载模式
                r = FileResponse(f, as_attachment=True, filename=f"{quote(mid)}.jpg")
                return r
            else:
                # 预览模式
                r = FileResponse(f, as_attachment=False, filename=f"{mid}")
                return r
        except Exception as e:
            # print(e)
            return response(503, "未找到该文件", "")



#检测历史数据列表
class LIstApi(APIView):
    def get(self, request):
        # 列表
        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)

        page, pagesize = pageGet(request)
        # 计算分页值
        start_page = page * pagesize - pagesize  # 计算每一页显示内容的范围
        end_page = page * pagesize

        #构建搜索参数
        dic = {}
        username = request.query_params.get("username", "")
        model = request.query_params.get("model", "")
        files_name = request.query_params.get("files_name", "")
        file_name = request.query_params.get("file_name", "")

        if username:
            dic['username'] = username
        if model:
            dic['model'] = model
        if files_name:
            dic['files_name'] =files_name
        if file_name:
            dic['file_name'] = file_name



        # 管理员显示所有
        if token_dic["data"]['level'] == 10:
            pass
        else:
            # 用户显示自己的
            dic['username'] = token_dic['data']['username']

        datas = models.DetectionModel.objects.filter(**dic).order_by('-id')[start_page:end_page].values()  # 从数据库中提取数据
        result = []
        for i in datas:
            i['CreatedAt'] = i['CreatedAt'].astimezone(shanghai_tz).strftime("%Y-%m-%d %H:%M:%S")
            i['UpdatedAt'] = i['UpdatedAt'].astimezone(shanghai_tz).strftime("%Y-%m-%d %H:%M:%S")
            result.append(i)

        # 查询总数据条数
        total = models.DetectionModel.objects.filter(**dic).count()
        return response(200, "查询成功", {
            "data": result,
            "total": total
        })

    def delete(self, request):
        '''删除'''
        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)

        ids = request.query_params.get("id")
        if ids == "":
            data = {'code': 503, "msg": "请选择需要删除的数据", 'data': ""}
            return JsonResponse(data)
        ids = [i for i in ids.split(",") if i]

        if token_dic["data"]['level'] == 10:
            # 管理员删除所有的
            Obj = models.DetectionModel.objects.filter(id__in=ids)
        else:
            # 用户只能删除自己的
            Obj = models.DetectionModel.objects.filter(id__in=ids, username=token_dic['data']['username'])


        count = Obj.count()
        if not Obj.exists():  # 不存在的状态
            data = {'code': 503, "msg": "数据不存在", 'data': ""}
            return JsonResponse(data)
        for i in Obj.values():
            try:
                os.remove(i['path_handle'])
            except Exception as e:
                print("删除文件时出现了错误")

        Obj.delete()  # 进行删除
        data = {'code': 200, "msg": f"成功删除了{count}条数据", 'data': ""}
        return JsonResponse(data)



#获取数据集范围
def get_slice_count(nii_file_path):
    img = nib.load(nii_file_path)
    return img.shape[2]


#获取可使用的数据集
class dataFileList(APIView):
    def get(self, request):
        modelList = ["MSF-TransUNet", "SCFG-Net"]
        result = {

        }
        for item in modelList:

            # 获取数据集列表
            filesList = os.listdir(f"app01/model/{item}")

            dic = {}
            for i in filesList:
                # 获取数据集下文件列表
                fileList = os.listdir(f"app01/model/{item}/{i}")
                dic[i] = []

                for file in fileList:
                    # 只获取文件名中有gt的
                    if not re.search("gt", file):
                        continue
                    #获取可设置的范围
                    count = get_slice_count(f"app01/model/{item}/{i}/{file}")
                    dic[i].append({
                        "file": file,
                        "count": count
                    })
                    # print(file,count)

            result[item] = dic

        return response(200, "查询成功", result)

# 检测
class Detection(APIView):

    # 进行检测
    def post(self, request):
        # 获取用户凭证
        token_dic, err = ParseToekn(request.META.get('HTTP_AUTHORIZATION'))
        if err != None:
            return response(401, "请重新登录", None)


        #模型
        model = request.data.get('model',"")
        if model == "":
            data = {'code': 503, "msg": "请选择模型", 'data': ""}
            return JsonResponse(data)
        #文件夹
        files_name = request.data.get('files_name',"")
        if files_name == "":
            data = {'code': 503, "msg": "请选择数据集", 'data': ""}
            return JsonResponse(data)

        #文件
        file_name = request.data.get('file_name',"")
        if file_name == "":
            data = {'code': 503, "msg": "请选择文件", 'data': ""}
            return JsonResponse(data)

        #范围
        slice_count = request.data.get('slice_count',"-1")
        if slice_count != "-1":
            slice_count = int(slice_count)
        else:
            slice_count = 1


        #根据模型使用不同的检测方法
        #拼接路径
        gt = f"app01/model/{model}/{files_name}/{file_name}"
        pred = re.sub("gt","pred",gt)
        #判断文件是否存在
        if not os.path.exists(gt):
            data = {'code': 503, "msg": "文件不存在", 'data': ""}
            return JsonResponse(data)
        if not os.path.exists(pred):
            data = {'code': 503, "msg": "辅助文件不存在", 'data': ""}
            return JsonResponse(data)

        max_slice_count = get_slice_count(gt)
        if max_slice_count <= slice_count:
            data = {'code': 503, "msg": "切片范围超过数据最大范围", 'data': ""}
            return JsonResponse(data)

        if slice_count == 0:
            slice_count = max_slice_count // 2


        #生成图片id
        mid = str(uuid.uuid4())
        path_handle = f"file/img/{mid}.jpg"
        #传入数据 调用模型
        if files_name == "ACDC":
            vis_acdc.prediction(gt, pred, slice_count, path_handle)
        elif files_name == "Synapse":
            vis_synapse.prediction(gt, pred, slice_count, path_handle)
        else:
            data = {'code': 503, "msg": "模型不存在", 'data': ""}
            return JsonResponse(data)


        # visualizeINvue.visualize_slice_and_prediction(gt,pred,path_handle,slice_count)



        #将数据保存到数据库中
        dic = {
            "username":token_dic["data"]["username"],
            "uid":token_dic["data"]["uid"],
            "model":model,
            "files_name":files_name,
            "file_name":file_name,
            "slice_count":slice_count,
            "mid_handle":mid,
            "path_handle":path_handle,
        }
        models.DetectionModel.objects.create(**dic)
        #返回图片数据
        return response(200, "检测完成", mid)




