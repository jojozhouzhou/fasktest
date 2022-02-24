from application import app
from common.libs.Herper import ops_render
from common.libs.log.LogService import LogService


@app.errorhandler(404)
def error_404(e):
    """ 拦截全局404异常 """
    LogService.addErrorLog(str(e))
    return ops_render("error/error.html", {"msg": "啊呀！！！页面走丢失啦"})


@app.errorhandler(Exception)
def error_500(e):
    """ 拦截全局异常 """
    LogService.addErrorLog(str(e))
    return ops_render("error/error.html", {"msg": str(e)})
