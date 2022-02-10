# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect
from common.libs.Herper import *
from common.libs.Resourt import *
from common.libs.UrlManage import UrlManage
from common.models.user import User
from application import app

route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    req = request.values
    page = int(req["page"]) if ("page" in req and req["req"]) else 1
    query = User.query
    page_params = {
        "total": query.count(),
        "page_size": app.config["PAGE_SIZE"],
        "page": page,
        "display": app.config["PAGE_DISPLAY"],
        "url": "/account/index"
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


@route_account.route("/set")
def set():
    return ops_render("account/set.html")
