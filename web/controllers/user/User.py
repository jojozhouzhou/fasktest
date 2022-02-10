# -*- coding: utf-8 -*-
import json

from flask import Blueprint, render_template, request, jsonify, make_response, redirect, g

from application import app
from common.libs.Herper import ops_render
from common.libs.UrlManage import UrlManage
from common.libs.user.UserService import UserService
from common.libs.Resourt import *
from common.models.user import User, db

route_user = Blueprint('user_page', __name__)


@route_user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("user/login.html")
    else:
        errorMsg = "登录成功"
        code = 200
        req = request.values
        res = {"code": code, "msg": errorMsg, "data": {}}
        login_name = req["login_name"] if "login_name" in req else ""
        login_pwd = req["login_pwd"] if "login_pwd" in req else ""
        if login_name == "":
            res["code"] = 500
            res["msg"] = "请输入登录用户名"
            return res
        elif login_pwd == "":
            res["code"] = 500
            res["msg"] = "请输入登录密码"
            return res

        user_info = User.query.filter_by(login_name=login_name).first()
        if not user_info:
            res["code"] = 500
            res["msg"] = "用户名或密码错误"
            return res
        user_pwd = user_info.login_pwd
        pwd_salt = user_info.login_salt
        input_pwd = UserService.genePwd(login_pwd, pwd_salt)
        if user_pwd != input_pwd:
            res["code"] = 500
            res["msg"] = "用户名或密码错误"
            return res

        # 配置返回，页面需要的值存入cookie
        response = make_response(json.dumps(res))
        response.set_cookie(app.config["AUTH_COOKIE_NAME"],
                            "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))
        return response


@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return ops_render("user/edit.html", {"current": "edit"})
    else:
        req = request.values
        nickname = req["nick_name"]
        email = req["email"]
        user_info = g.current_user
        user_info.nickname = nickname
        user_info.email = email
        db.session.add(user_info)
        db.session.commit()
        return jsonify(req)


@route_user.route("/reset_pwd", methods=["GET", "POST"])
def resetPwd():
    method = request.method
    if method == "GET":
        return ops_render("user/reset_pwd.html", {"current": "reset_pwd"})
    req = request.values
    old_password = req["old_password"]
    new_password = req["new_password"]
    user_info = g.current_user
    login_salt = user_info.login_salt
    new_password_code = UserService.genePwd(new_password, login_salt)
    user_info.login_pwd = new_password_code
    db.session.add(user_info)
    db.session.commit()

    # 配置返回，页面需要的值存入cookie
    res = success("用户密码修改成功")
    response = make_response(json.dumps(res))
    response.set_cookie(app.config["AUTH_COOKIE_NAME"],
                        "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))

    return response

@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManage.buildUrl("/user/login")))
    response.delete_cookie(app.config["AUTH_COOKIE_NAME"])
    return response
