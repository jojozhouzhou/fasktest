import os
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=None)
        self.config.from_pyfile('config/base_setting.py')
        environ = os.environ
        if "ops_config" in environ:
            self.config.from_pyfile('config/%s_setting.py' % environ['ops_config'])

        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__, template_folder=os.getcwd() + "/web/templates/", root_path=os.getcwd())
# 解决flask接口中文数据编码问题
app.config['JSON_AS_ASCII'] = False
manager = Manager(app)

# 函数模版，用来供html页面调用
from common.libs.UrlManage import UrlManage

app.add_template_global(UrlManage.buildStaticUrl, "buildStaticUrl")
app.add_template_global(UrlManage.buildUrl, "buildUrl")
