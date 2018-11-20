from flask_wtf import Form
from wtforms import Form

from wtforms import StringField, validators, PasswordField, ValidationError
from werkzeug.security import check_password_hash
from flask import g
# 注册提交的数据进行验证
from apps.models.buyer_model import BuyerUser
from apps.pli import api_redis


# 用户注册的form验证
class BuyerRegisterForm(Form):
    username = StringField(label="用户名",
                           validators=[validators.InputRequired(message='请填写用户名'),
                                       validators.Length(max=11, message="用户名不宜过长"),
                                       validators.Length(min=3, message="用户名不宜过短"),
                                       ])
    tel = StringField(label='用户电话',
                      validators=[validators.InputRequired(message='请填写电话'),
                                  validators.Length(max=11, message="请输入准确的手机号"),
                                  validators.Regexp(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$',
                                                    message="请输入正确的手机号码")
                                  ])
    sms = StringField(label="验证码",
                      validators=[validators.InputRequired(message="请输入验证码"),
                                  ]
                      )
    password = PasswordField(label="密码",
                             validators=[
                                 validators.InputRequired(message='请填写密码'),
                                 validators.Length(max=16, message="密码最好不要太长"),
                                 validators.Length(min=6, message="密码长度最少6位")
                             ])

    # 自定义验证函数,验证当前商家输入的电话是否已经被注册过
    def validate_tel(self, field):
        seller_phone = field.data
        reg_phone = BuyerUser.query.filter(BuyerUser.tel == seller_phone).first()
        if reg_phone:
            raise ValidationError("该电话已被注册")

    def validate_username(self, field):
        usernmae = field.data
        reg_username = BuyerUser.query.filter(BuyerUser.username == usernmae).first()
        if reg_username:
            raise ValidationError("该用户名已被使用,请更换用户名")

    # 验证码的自定义验证
    def validate_sms(self, value):
        # 查询redis数据库中的验证码
        redis_sms = api_redis.get("sms_{}".format(self.tel.data))

        if not redis_sms:
            raise ValidationError("没有验证码,请先获取验证码")
        if redis_sms.decode("ascii") != value.data:
            raise ValidationError("验证码不正确")



# 登录过来的数据进行验证
class LoginSellerForm(Form):
    name = StringField(label='用户登录名',
                       validators=[validators.DataRequired(message='请填写用户名')],
                       )
    password = PasswordField(label="登录密码",
                             validators=[
                                 validators.DataRequired(message='请填写密码'),
                                 validators.Length(max=16, message="密码最好不要太长"),
                                 validators.Length(min=6, message="密码长度最少6位")
                             ],
                             )

    def validate_password(self, value):
        get_password = value.data
        # 先查看用户名是否存在
        db_username = BuyerUser.query.filter(BuyerUser.username == self.name.data).first()
        # 根据用户名,查看密码是否正确
        if db_username:
            num = db_username.check_password(get_password)
            if not num:
                raise ValidationError("用户名或者密码错误")
        else:
            raise ValidationError("用户名或者密码错误")


# 用户地址信息的添加form
class AddAddressForm(Form):
    name = StringField(label='收货人姓名',
                       validators=[validators.DataRequired(message='请填写用户名'),
                                   validators.Length(max=20, message="请填写正确的收货人姓名"),
                                   validators.Length(min=2, message="收货人姓名至少2位")
                                   ], )
    tel = StringField(label='收货人电话',
                      validators=[validators.InputRequired(message='请填写电话'),
                                  validators.Length(max=11, message="请输入准确的手机号"),
                                  validators.Regexp(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$',
                                                    message="请输入正确的手机号码")
                                  ])
    provence = StringField(label="省")
    city = StringField(label="市", validators=[
        validators.DataRequired(message="请填写所在的城市")])
    area = StringField(label="区县", validators=[
        validators.DataRequired(message="请填写所在的区县")])
    detail_address = StringField(label="详细地址", validators=[
        validators.DataRequired(message="请填写所在的区县")])
