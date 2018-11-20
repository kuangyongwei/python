# token的认证装饰器
from functools import wraps

from flask import request, jsonify, current_app,g
from itsdangerous import Serializer, BadSignature, SignatureExpired

from apps.models.buyer_model import BuyerUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def token_auth(f):
    @wraps(f)  # 该函数是python自带的函数,目的是保存想要装饰的函数的源信息
    def fun(*args, **kwargs):
        token = request.cookies.get("x-token")
        if not token:
            return jsonify({"status": "false", "message": "最好重新登录"})
        try:
            s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
            data = s.loads(token)
        except BadSignature:
            return jsonify({'status': "false", 'message': '登录无效'})
        except SignatureExpired:
            return jsonify({'status': "false", 'message': '登录超时'})
        # cookie携带的信息有效,根据值查询当前用户
        current_user = BuyerUser.query.filter(BuyerUser.username == data["username"]).first()
        g.current_user = current_user
        return f(*args, **kwargs)
    return fun
