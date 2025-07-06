from django.http import JsonResponse


def response(code,msg,data):
    # 制作返回给前端的json
    data = {
        "code": code,
        "msg": msg,
        "data": data
    }

    return JsonResponse(data)  # 以json格式返回数据