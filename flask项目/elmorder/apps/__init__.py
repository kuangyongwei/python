from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


# 蓝图注册的函数
def reg_blueprint(app):
    from apps.cms import cms_bp
    app.register_blueprint(cms_bp)


# 买家buyer蓝图的注册
def api_reg_blueprint(app):
    from apps.apis import api_bp
    app.register_blueprint(api_bp)


# 数据库的配置
def models_conf(app):
    from apps.models import db
    db.init_app(app)


# session的注册
def reg_session(app):
    from flask_session import Session
    Session(app)


# 创建后台商家管理app
def create_app():
    # 1. 创建app,这个app现在仅仅是支持WSGI协议的接口而已
    app = Flask(__name__)

    # 2. 进行配置app信息
    app.config.from_object('apps.settings.DevConfig')
    # 3.数据库进行配置
    models_conf(app)
    # 4.session的注册
    reg_session(app)
    # login的管理
    login_manager.init_app(app)
    login_manager.login_view = "cms.login"

    # 5.蓝图的注册
    reg_blueprint(app)

    return app


# 创建client用户的app
def create_api_app():
    app = Flask(__name__, static_url_path='', static_folder='./web_client/')
    # app.run()
    # buyer买家app的配置
    app.config.from_object("apps.settings.Buyer_DevConfig")
    # 数据库的配置,与卖家的app一样用相同的数据库
    models_conf(app)

    # 蓝图的注册
    api_reg_blueprint(app)
    return app
