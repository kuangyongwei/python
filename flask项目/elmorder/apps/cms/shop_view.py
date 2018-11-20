from flask import request, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from apps.cms import cms_bp
from apps.models import db
from apps.pli import set1_uuid, form_to_model
from apps.forms.shop_form import SellerShopForm

# 商家店铺信息添加
from apps.models.shop_model import SellerShop


@cms_bp.route("/add_shop/", endpoint="add_shop", methods=['GET', 'POST'])
@login_required
def add_shop():
    # 获取当前商家对象
    shop_form = SellerShopForm(request.form)
    if request.method == "POST" and shop_form.validate():
        # 提交过来的数据合法
        aa = request.form
        shop = SellerShop()
        shop.set_attrs(shop_form.data)
        shop.pub_id = set1_uuid()
        shop.seller = current_user
        db.session.add(shop)
        db.session.commit()
        # 商铺数据库添加成功
        return "添加信息成功"
    return render_template("seller_shop.html", form=shop_form)


# 商家店铺的展示
@cms_bp.route("/show_shop/", endpoint="show_shop", methods=['GET', 'POST'])
@login_required
def show_shop():
    # 得到当前用户信息
    user = current_user
    # 查询当前用户有哪些商铺
    user_shop = user.shop
    stores = user_shop
    return render_template('show_shop.html', stores=stores)


def check_pub_id(pub_id):
    shop = SellerShop.query.filter(SellerShop.seller == current_user, SellerShop.pub_id == pub_id).first()
    if not shop:
        return abort(redirect(url_for("cms.index")))
    return shop


# 当店铺名称被点击后,达到查看店铺信息的目的，传递一个当前店铺pub_id的信息
@cms_bp.route("/update_shop/<pub_id>", endpoint="update_shop", methods=['GET', 'POST'])
@login_required
def update_shop(pub_id):
    shop = check_pub_id(pub_id)
    shop_form = SellerShopForm(request.form)
    if request.method == "GET":
        # 检查当前商铺是否存在,不存在,返回首页,存在,返回当前商铺shop对象
        shop_form = SellerShopForm(data=dict(shop))
        return render_template('seller_shop.html', flags="店铺", shop=shop, form=shop_form)
    elif request.method == 'POST' and form_to_model(shop_form, shop):
        return redirect(url_for('cms.show_shop'))
    return render_template('seller_shop.html', flags="店铺", shop=shop, form=shop_form)


