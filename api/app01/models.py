from django.db import models

# Create your models here.


#用户信息表
class UserModel(models.Model):
    '''用户信息表'''

    #注册时间
    CreatedAt=models.DateTimeField(verbose_name='注册时间',auto_now_add=True)    #年月日    自动保存为创建时间

    #最近修改时间
    UpdatedAt=models.DateTimeField(verbose_name='最近修改时间',auto_now=True)  #年月日 时分秒  自动保存为最近修改时间

    #用户id
    uid = models.CharField(verbose_name="用户id",max_length=64)
    #用户名
    username=models.CharField(verbose_name='用户名',unique=True,max_length=32)
    #密码
    password=models.CharField(verbose_name='密码',max_length=64)
    #昵称
    name = models.CharField(verbose_name="昵称",max_length=32)
    #用户手机
    phone=models.CharField(verbose_name='用户手机',max_length=11,default='')

    #用户头像
    img = models.CharField(verbose_name='用户头像',max_length=128,default='')

    #限权等级
    level=models.IntegerField(verbose_name='用户等级',default=1)


#检测管理
class DetectionModel(models.Model):
    #上传时间
    CreatedAt=models.DateTimeField(verbose_name='上传时间',auto_now_add=True)    #年月日    自动保存为创建时间
    #最近修改时间
    UpdatedAt=models.DateTimeField(verbose_name='最近修改时间',auto_now=True)  #年月日 时分秒  自动保存为最近修改时间

    #上传人
    username=models.CharField(verbose_name='用户账号',max_length=64)
    #用户uid
    uid = models.CharField(verbose_name="用户id",max_length=64)




    
    #模型
    model =  models.CharField(verbose_name='模型',max_length=128)
    #文件夹
    files_name = models.CharField(verbose_name='文件夹',max_length=128)
    #文件
    file_name = models.CharField(verbose_name='文件',max_length=128)
    #范围
    slice_count = models.IntegerField(verbose_name='范围')

    #检测后的图片id
    mid_handle =models.CharField(verbose_name='检测后的图片id',max_length=64,default='')
    #处理后图片
    path_handle = models.CharField(verbose_name='检测后图片路径',max_length=128,default='')


    
    


#数据集添加请求表
class DataAddAskModel(models.Model):
    #上传时间
    CreatedAt=models.DateTimeField(verbose_name='上传时间',auto_now_add=True)    #年月日    自动保存为创建时间
    #最近修改时间
    UpdatedAt=models.DateTimeField(verbose_name='最近修改时间',auto_now=True)  #年月日 时分秒  自动保存为最近修改时间

    #用户账号
    username=models.CharField(verbose_name='用户名',max_length=32)
    #用户uid
    uid = models.CharField(verbose_name="用户id",max_length=64)
    #标题
    title = models.CharField(verbose_name="标题",max_length=255)
    #说明
    describe= models.CharField(verbose_name="说明",max_length=255)
    #数据集来源
    source = models.CharField(verbose_name="数据集来源",max_length=255)
    #状态       等待管理员处理/管理员处理中/已完成请求/处理失败
    state = models.CharField(verbose_name="状态",max_length=32)
    #管理员回复
    admin_reply = models.CharField(verbose_name="管理员回复",max_length=255)
