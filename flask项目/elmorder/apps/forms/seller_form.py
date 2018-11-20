from wtforms import Form
from apps.models.seller_model import SellerLoginModel
from wtforms import StringField, validators, PasswordField, ValidationError
from werkzeug.security import check_password_hash


# 注册提交的数据进行验证
class RegisterSellerForm(Form):
    seller_phone = StringField(label='商家电话',
                               validators=[validators.InputRequired(message='请填写电话'),
                                           validators.Length(max=11, message="请输入准确的手机号")
                                           ],
                               render_kw={'class': 'form-control', 'placeholder': '请输入手机号'})
    password = PasswordField(label="密码",
                             validators=[
                                 validators.InputRequired(message='请填写密码'),
                                 validators.Length(max=16, message="密码最好不要太长"),
                                 validators.Length(min=6, message="密码长度最少6位")
                             ],
                             render_kw={'class': 'form-control', 'placeholder': '请输入密码'})
    password2 = PasswordField(label='确认密码',
                              validators=[
                                  validators.InputRequired(message='请填写确认密码'),
                                  validators.EqualTo('password', message='两次密码不一致')
                              ],
                              render_kw={'class': 'form-control', 'placeholder': '请输入确认密码'})

    # 自定义验证函数,验证当前商家输入的电话是否已经被注册过
    def validate_seller_phone(self, field):
        seller_phone = field.data
        reg_phone = SellerLoginModel.query.filter(SellerLoginModel.seller_phone == seller_phone).first()
        if reg_phone:
            raise ValidationError("该电话已被注册")


# 登录过来的数据进行验证
class LoginSellerForm(Form):
    seller_phone = StringField(label='商家电话',
                               validators=[validators.DataRequired(message='请填写电话')],
                               render_kw={'class': 'form-control', 'placeholder': '请输入确认密码'}
                               )
    password = PasswordField(label="密码",
                             validators=[
                                 validators.DataRequired(message='请填写密码'),
                                 validators.Length(max=16, message="密码最好不要太长"),
                                 validators.Length(min=6, message="密码长度最少6位")
                             ],
                             render_kw={'class': 'form-control', 'placeholder': '请输入确认密码'}
                             )

