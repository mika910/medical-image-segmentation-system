import jwt
import datetime
import time

from app01.myTools.timetz import  shanghai_tz

jwt_outtime=30        #设置过期时间
jwt_Issuer = "admin"     #设置签发人
jwt_key="admin1156"    #加密密钥

#加密
def GenToken(username,uid,level):
    dic = {
        'exp': datetime.datetime.now(shanghai_tz) + datetime.timedelta(days=jwt_outtime),  # 过期时间
        'iat': datetime.datetime.now(shanghai_tz),                               #  开始时间
        'iss': jwt_Issuer,                                            # 签名
        'data': {  # 内容，一般存放该用户id和开始时间
            'username': username,
            "uid":uid,
            'level': level,
        },
    }
    s = jwt.encode(dic, jwt_key, algorithm='HS256')  # 加密生成字符串
    return s

#解密
def ParseToekn(token):
    try:
        s = jwt.decode(token, jwt_key, issuer=jwt_Issuer, algorithms=['HS256'])  # 解密，校验签名
        current_milli_time = lambda: int(round(time.time() ))         #时间验证 看看token过期了没有
        if current_milli_time() > s["exp"]:
            return "", "token已过期"
    except Exception as e:
        print(e)
        return "","解密失败"
    return s,None




