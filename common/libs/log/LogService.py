import json
from common.models.AppAccessLog import AppAccessLog
from common.models.AppErrorLog import AppErrorLog
from flask import request, g
from common.libs.Herper import getCurrentDate
from application import db


class LogService():
    @staticmethod
    def addAccessLog():
        target = AppAccessLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.ip = request.remote_addr
        target.query_params = json.dumps(request.values.to_dict())
        if "current_user" in g and g.current_user is not None:
            target.uid = g.current_user.uid
        target.ua = request.headers.get("User-Agent")
        target.create_time = getCurrentDate()
        db.session.add(target)
        db.session.commit()
        return True

    @staticmethod
    def addErrorLog(e):
        target = AppErrorLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.ip = request.remote_addr
        target.query_params = json.dumps(request.values.to_dict())
        target.content = e
        if "current_user" in g and g.current_user is not None:
            target.uid = g.current_user.uid
        target.ua = request.headers.get("User-Agent")
        target.create_time = getCurrentDate()
        db.session.add(target)
        db.session.commit()
        return True
