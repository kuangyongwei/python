import random
from functools import wraps

from flask import g, current_app, make_response
from flask import jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from apps.apis import api_bp
from apps.forms.buyer_reg_form import BuyerRegisterForm, LoginSellerForm, AddAddressForm
from apps.models import db
from apps.models.buyer_model import BuyerUser, BuyerAddressModel
from apps.models.shop_model import SellerShop
from apps.pli import api_redis
from apps.pli.token_validate import token_auth


# 商铺列表的展示api
@api_bp.route('/shop_list/', methods=["GET"])
def shop_list():
    # 查询店铺表全部信息
    shop_list = SellerShop.query.all()  # [<shop>, <shop>]
    data = [{**dict(shop), "id": shop.pub_id, "shop_rating": shop.shop_rating} for shop in shop_list]
    # print(data[0])
    return jsonify(data)


# 商铺信息的展示api
@api_bp.route('/shop/', methods=["GET"])
def shop():
    # 得到传过来的SellerShop的pub_id
    shop_pid = request.args.get("id")
    # 通过当前id,找到当前店铺的全部菜单分类
    shop = SellerShop.query.filter(SellerShop.pub_id == shop_pid).first()
    category_list = shop.categories
    data = {**dict(shop), "id": shop.pub_id,
            "commodity": [
                {**dict(category), "goods_list": [{**dict(x), "goods_id": x.goods_id, } for x in category.foods]} for
                category in category_list]}
    return jsonify(data)


# 短信验证的api
@api_bp.route('/sms/', methods=["GET"])
def sms():
    tel = request.args.get("tel")
    if tel:
        # 随机产生一个验证码
        yzm = ''.join([str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) for _ in range(4)])
        print("产生的验证码是: {}".format(yzm))
        # 对保存到redis的数据进行加工
        tel = "sms_{}".format(tel)
        api_redis.setex(tel, yzm, current_app.config.get("SMS_LIFETIME"))
        return jsonify({"status": "true", "message": "成功发送验证码"})
    else:
        return jsonify({"status": "false", "message": "请先输入电话号码"})


# 用户注册的视图函数
@api_bp.route('/register/', endpoint="register", methods=["POST"])
def register():
    form = BuyerRegisterForm(request.form)
    if form.validate():
        # 如果数据合法,保存到数据库
        buyer_user = BuyerUser()
        buyer_user.set_attrs(form.data)
        db.session.add(buyer_user)
        db.session.commit()
        return jsonify({"status": 'true', "message": "注册成功"})
    else:
        return jsonify(
            {"status": 'false', "message": "".join(["{}:{}".format(k, v[0]) for k, v in form.errors.items()])})


"""
登录成功过后,需要给该用户颁发一个token的令牌,
    因为该令牌需要json格式,该格式需要签名,需要用到python中的TimedJSONWebSignatureSerializer as/重命名 Serializer
    该令牌有一个过期时间, 
    加密方式为对称加密:     
    用法
    # 该对象为一个序列化器,装修/装饰为一个json格式
        s = Serializer(secret_key='abc', expires_in=3600 * 24)  # 设置秘钥和过期时间
        token = s.dump({"username": form.data.name})
        return jsonify("token":token.decode("utf-8))
"""


# 用户登录的视图函数
@api_bp.route('/login/', endpoint="login", methods=["POST"])
def login():
    form = LoginSellerForm(request.form)
    if form.validate():
        # 登录成功
        s = Serializer(secret_key=current_app.config["SECRET_KEY"], expires_in=3600)
        data = s.dumps({"username": form.name.data})
        # 需要将itoken设置为cookie
        response = jsonify({"status": "true", "message": "登录成功", "username": form.name.data})
        response.set_cookie("x-token", data.decode("ascii"))
        return response
    else:
        return jsonify({"status": "false", "message": "登录失败"})














