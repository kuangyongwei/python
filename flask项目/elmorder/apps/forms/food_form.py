from wtforms import Form, RadioField, FloatField, IntegerField, BooleanField, DecimalField, SelectField
from wtforms import StringField, validators, ValidationError
from flask_login import current_user

# 菜单类验证
from apps.models.shop_model import SellerShop


class MenuCategoryForm(Form):
    name = StringField(label="菜品分类名", validators=[
        validators.InputRequired(message="请填写菜品分类"),
        validators.Length(max=32, message="菜品分类名称不易过长")
    ],
                       render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类名称'}
                       )
    description = StringField(label="菜品分类描述",
                              render_kw={'class': 'form-control', 'placeholder': '描述信息'}
                              )
    type_accumulation = StringField(label="菜品分类编号",
                                    validators=[
                                        validators.Length(max=16, message="不能超过16字符"),
                                    ],
                                    render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类编号'},
                                    )
    # 是否默认
    is_default = BooleanField(label="是否默认", default=False)


# 菜品表验证
class MenuFoodForm(Form):
    goods_name = StringField(label="菜品名称", validators=[
        validators.InputRequired(message="请填写菜品名称"),
        validators.Length(max=32, message="菜品名称最大32位"),
        validators.Length(min=3, message="菜品名称不宜过短")
    ], render_kw={'class': 'form-control', 'placeholder': '请输入菜品名称'}, )

    # shop_id = IntegerField(label="归属店铺",
    #                        render_kw={'class': 'form-control', "display": "hidden"},
    #                        )
    category_id = SelectField(label="选择菜品分类",
                              coerce=int,
                              validators=[validators.DataRequired(message="请必须选择菜品分类")],
                              render_kw={'class': 'form-control'},
                              )
    goods_price = DecimalField(label="菜品价格",
                               render_kw={'class': 'form-control', 'placeholder': '请输入菜品价格'}
                               )
    description = StringField(label="菜品描述", validators=[
        validators.Length(max=128, message="菜品描述最大128位"),
    ], render_kw={'class': 'form-control', 'placeholder': '请输入菜品描述'},
                              )
    tips = StringField(label="菜品提示信息",
                       render_kw={'class': 'form-control', 'placeholder': '菜品提示信息'}
                       )

    goods_img = StringField(label='菜品图片', id="image-input",)

    def __init__(self, *args, **kwargs):
        # 查询得到当前的商铺
        self.abc = kwargs["shop_id"]
        shop = SellerShop.query.filter(SellerShop.id == self.abc).first()
        super(MenuFoodForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(x.id, x.name) for x in shop.categories]
