# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect
from common.libs.Herper import *
from common.libs.Resourt import *
from common.libs.user.UserService import UserService
from common.libs.UrlManage import UrlManage
from common.models.user import User, db
from application import app

route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    req = request.values
    page = int(req["p"]) if ("p" in req and req["p"]) else 1
    query = User.query
    full_path = request.full_path
    page_params = {
        "total": query.count(),
        "page_size": app.config["PAGE_SIZE"],
        "page": page,
        "display": app.config["PAGE_DISPLAY"],
        "url": full_path.replace("&p={}".format(page),"")
    }
    pages = iPagination(page_params)
    offset = (page - 1) * page_params["page_size"]
    limit = page_params["page_size"] * page
    list = query.order_by(User.uid.desc()).all()[offset:limit]
    return ops_render("account/index.html", {"list": list, "pages": pages})


@route_account.route("/info")
def info():
    # values可以去到所有请求的所有参数
    res = request.values
    # args可以精确去到get方法的所有参数
    args = request.args
    if "id" not in args:
        return redirect(UrlManage.buildUrl("/account/index"))
    id = args.get("id")
    user_info = User.query.filter_by(uid=id).first()
    return ops_render("account/info.html", {"user_info": user_info})


@route_account.route("/set", methods=["GET", "POST"])
def set():
    method = request.method
    req = request.values
    if method == "GET":
        res = {"userinfo": None}
        if "id" not in req:
            return ops_render("account/set.html", res)
        id = req["id"]
        user_info = User.query.filter(User.uid == id).first()
        if user_info:
            res["userinfo"] = user_info
            return ops_render("account/set.html", res)
        return redirect(UrlManage.buildUrl("/account/index"))

    nickname = req["nickname"] if "nickname" in req else ""
    mobile = req["mobile"] if "mobile" in req else ""
    email = req["email"] if "email" in req else ""
    login_name = req["login_name"] if "login_name" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""
    id = int(req["id"]) if "id" in req else "0"

    # 登录名称和邮箱不得重复
    login_name_has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if login_name_has_in:
        return fail("用户名已存在，请重新输入")
    login_email_has_in = User.query.filter(User.email == email, User.uid != id).first()
    if login_email_has_in:
        return fail("此邮箱已注册，请重新输入")
    if id:
        model_user = User.query.filter_by(uid=id).first()
        model_user.updated_time = getCurrentDate()
    else:
        model_user = User()
        model_user.login_salt = UserService.geneSalt(16)
    model_user.login_name = login_name
    model_user.nickname = nickname
    if login_pwd != "******":
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
        model_user.created_time = getCurrentDate()
    model_user.email = email
    model_user.mobile = mobile
    model_user.sex = 1
    model_user.status = 1

    db.session.add(model_user)
    db.session.commit()
    return success(data=req)
