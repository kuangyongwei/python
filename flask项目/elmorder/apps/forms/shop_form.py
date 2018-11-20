from wtforms import Form, FloatField, BooleanField, DecimalField
from wtforms import StringField, validators, ValidationError

from apps.models.shop_model import SellerShop


class SellerShopForm(Form):
    shop_name = StringField(label="店铺名称", validators=[
        validators.InputRequired(message="请填写店铺名称"),
        validators.Length(max=32, message="店铺名称不易过长"),
        validators.Length(min=3, message="店铺名称至少3位")
    ],
                            render_kw={'class': 'form-control', 'placeholder': '请输入店铺名称'}
                            )
    shop_img = StringField(label='商家Logo', id="image-input",)

    brand = BooleanField(label="是否是品牌", default=False
                         )
    on_time = BooleanField(label="是否准时送达", default=True)
    fengniao = BooleanField(label="是否蜂鸟配送", default=True)
    bao = BooleanField(label="是否保险", default=False)

    piao = BooleanField(label="是否有发票", default=True)
    zhun = BooleanField(label="是否准标识", default=False)
    start_send = FloatField(label="起送价格",
                            validators=[validators.DataRequired(message="填写起送价格")],
                            render_kw={'class': 'form-control', 'placeholder': '配送费默认为0'}
                            )
    send_cost = DecimalField(label="配送费用",
                             validators=[validators.InputRequired(message="填写配送费用")],
                             render_kw={'class': 'form-control', 'placeholder': '请输入配送费用'},
                             )
    notice = StringField(label="店铺公告", validators=[
        validators.Length(max=210, message="公告过长")
    ], render_kw={'class': 'form-control'}, default='')
    discount = StringField(label="优惠信息", validators=[
        validators.Length(max=210, message="优惠信息过长")
    ], render_kw={'class': 'form-control'}, default='')

    # 自定义验证函数,验证当前商家输入的电话是否已经被注册过
    def validate_shop_name(self, field):
        a = field.data
        reg_name = SellerShop.query.filter(SellerShop.shop_name == a).first()
        if reg_name:
            raise ValidationError("该商铺名已经被注册,最好换一个")
