import os
from datetime import timedelta

from redis import Redis


class BaseConfig(object):
    SECRET_KEY = "abc"


def get_path():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


class DevConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\1python\python\\flask_projects\\elmorder\\elm2.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/elm2.sqlite'.format(get_path())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 设置sesion的配置
    SESSION_TYPE = 'redis'
    # 设置浏览器保存session的名字
    SESSION_COOKIE_NAME = "elc_session"
    SESSION_REDIS = Redis('192.168.205.132', port=6388)
    PERMANENT_SESSION_LIFETIME = 3600 * 7
    # session本地保存的前缀名
    SESSION_KEY_PREFIX = 'seller'


# 买家app所需的配置文件
class Buyer_DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/elm2.sqlite'.format(get_path())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "api_cms"
    SMS_LIFETIME = timedelta(seconds=5 * 60)  # 设置短信验证码在redis的过期时间
    CART_LIFETIME = timedelta(seconds=3600 * 24)


class ProductConfig(BaseConfig):
    DEBUG = False
