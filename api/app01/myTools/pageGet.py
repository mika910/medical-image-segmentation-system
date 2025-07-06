

def pageGet(req):
    page = req.query_params.get("page")
    pagesize = req.query_params.get("pagesize")

    try:
        page = int(page)
        pagesize = int(pagesize)
    except Exception as e:
        print("提交翻页参数错误",e)
        return 1,10

    return page,pagesize