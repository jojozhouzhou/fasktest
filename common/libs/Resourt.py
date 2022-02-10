res = {"code": 200, "msg": "", "data": {}}


def internal_error():
    res["code"] = 500
    res["msg"] = "服务器内部错误"
    return res


def fail(error_msg="执行失败"):
    res["code"] = 500
    res["msg"] = error_msg
    return res


def success(msg="执行成功"):
    res["code"] = 200
    res["msg"] = msg
    return res
