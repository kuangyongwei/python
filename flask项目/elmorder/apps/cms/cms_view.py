from apps.cms import cms_bp
from flask import render_template, request, redirect, url_for, session
from apps.forms.seller_form import RegisterSellerForm, LoginSellerForm
from apps.forms.shop_form import SellerShopForm
from apps.models.seller_model import SellerLoginModel
from apps.models import db
from flask_login import login_user, logout_user, login_required, current_user

from apps.models.shop_model import SellerShop


# 注册视图函数
@cms_bp.route("/reg/", endpoint="register", methods=['GET', 'POST'])
def register():
    form = RegisterSellerForm(request.form)
    if request.method == 'POST' and form.validate():
        seller = SellerLoginModel()
        # print(form.data)
        seller.set_attrs(form.data)
        db.session.add(seller)
        db.session.commit()
        # print(11)
        # print(form)
        return redirect(url_for("cms.login"))
    return render_template('register.html', form=form)


# 登录的视图函数
@cms_bp.route("/login/", endpoint="login", methods=['GET', 'POST'])
def login():
    form = LoginSellerForm(request.form)
    # 如果用户提交登录信息,以及数据验证合法的情况下
    if request.method == 'POST' and form.validate():
        # 1.判断用户在数据库是否存在
        seller = SellerLoginModel.query.filter(SellerLoginModel.seller_phone == form.seller_phone.data).first()
        # 用户存在,调用model里面的check_password方法,验证密码是否正确
        if seller and seller.check_password(form.password.data):
            login_user(seller)
            # print(current_user)
            return redirect(url_for('cms.show_shop'))
        else:
            form.password.errors = ["用户名或者密码错误"]
    print(1)
    # print(current_user)
    # return 'hello'
    return render_template("login.html", form=form)


# 注销的视图函数
@cms_bp.route("/logout/", endpoint="logout")
def logout():
    # 查看当前商家对象
    logout_user()
    return render_template('logout.html')


# 首页
@cms_bp.route("/index/", endpoint="index", methods=['GET', 'POST'])
@login_required
def index():
    print(session.get('elm_seller'))
    return render_template("seller_index.html")



