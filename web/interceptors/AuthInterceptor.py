import re
from application import app
from flask import request, render_template, redirect, g
from common.models.user import User
from common.libs.user.UserService import UserService
from common.libs.UrlManage import UrlManage


@app.before_request
def befor_request():
    ignore_urls = app.config["IGNORE_URLS"]
    ignore_check_login_urls = app.config["IGNORE_CHECK_LOGIN_URLS"]
    path = request.path

    pattern = re.compile("%s" % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    pattern = re.compile("%s" % "|".join(ignore_urls))
    if pattern.match(path):
        return
    check_result = check_login()
    if not check_result:
        return redirect(UrlManage.buildUrl("/user/login"))


def check_login():
    """ 判断用户是否已经登录 """
    cookies = request.cookies
    auth_cookie = cookies[app.config["AUTH_COOKIE_NAME"]] if app.config["AUTH_COOKIE_NAME"] in cookies else None
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False
    user_cookie_auth = auth_info[0]
    uid = auth_info[1]
    user_auth = ""
    try:
        user_info = User.query.filter_by(uid=uid).first()
        if user_info is None:
            return False
        user_auth = UserService.geneAuthCode(user_info)
        g.current_user = user_info
    except Exception as e:
        return False

    if user_auth == user_cookie_auth:
        return True
    return False
