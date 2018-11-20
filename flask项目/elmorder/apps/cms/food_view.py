from flask import request, render_template, abort, redirect, url_for, jsonify
from flask_login import login_required, current_user
from qiniu import Auth

from apps.cms import cms_bp
from apps.cms.shop_view import check_pub_id
from apps.forms.food_form import MenuCategoryForm, MenuFoodForm
from apps.models import db
from apps.models.food_model import MenuCategory, MenuFood
from apps.models.shop_model import SellerShop
from apps.pli import set2_uuid, form_to_model, set3_uuid


# 菜品分类的添加
@cms_bp.route('/add_category/<shop_id>', endpoint='add_category', methods=['GET', 'POST'])
@login_required
def add_cate(shop_id):
    # 查询当前菜单所属店铺名
    shop = SellerShop.query.filter(SellerShop.pub_id == shop_id).first()
    shop_name = shop.shop_name
    category_form = MenuCategoryForm(request.form)
    if request.method == 'POST' and category_form.validate():
        # 提交数据合法
        food_category = MenuCategory()
        food_category.set_attrs(category_form.data)
        food_category.pub_id = set2_uuid()
        food_category.shop_id = shop.pub_id
        db.session.add(food_category)
        db.session.commit()
        return "菜品分类表格"

    return render_template('add_category.html', form=category_form, flags="菜品分类", shop_name=shop_name)


# 菜品分类的展示
@cms_bp.route('/show_category/<shop_id>', endpoint='show_category', methods=['GET', 'POST'])
@login_required
def show_category(shop_id):
    # 得到当前商铺对象
    shop = SellerShop.query.filter(SellerShop.pub_id == shop_id).first()
    # 根据当前商铺查询菜品分类列表
    category_list = shop.categories
    return render_template("show_category.html", stores=category_list, shop_id=shop_id, shop_true_id=shop.id)


# 检查菜品分类信息
def check_food_category(shop_id, pub_id):
    food_category = MenuCategory.query.filter(MenuCategory.pub_id == pub_id, MenuCategory.shop_id == shop_id).first()
    if not food_category:
        return abort(redirect(url_for("cms.index")))
    return food_category


# 菜品分类的修改
@cms_bp.route('/update_category/<shop_id>/<pub_id>', endpoint='update_category', methods=['GET', 'POST'])
@login_required
def update_category(shop_id, pub_id):
    food_category = check_food_category(shop_id, pub_id)  # 菜单分类的对象
    food_category_form = MenuCategoryForm(request.form)  # 当客户修改某个菜品分类的时候,提交信息验证
    # 当为查看菜单的时候
    if request.method == "GET":
        food_category.id = str(food_category.id)
        food_category_form = MenuCategoryForm(data=dict(food_category))
        return render_template("add_category.html", form=food_category_form)
    elif request.method == "POST" and form_to_model(food_category_form, food_category):
        return redirect(url_for("cms.show_category", shop_id=shop_id))


def check_shop_id(shop_id):
    shop = SellerShop.query.filter(SellerShop.seller == current_user, SellerShop.id == shop_id).first()
    if not shop:
        return abort(redirect(url_for("cms.index")))
    return shop


# 菜品的添加
@cms_bp.route('/add_food/<shop_id>', endpoint='add_food', methods=['GET', 'POST'])
@login_required
def add_food(shop_id):
    shop = check_shop_id(shop_id)
    form = MenuFoodForm(request.form, shop_id=shop_id)
    if request.method == "POST" and form.validate():
        # 数据合法
        food = MenuFood()
        food.set_attrs(form.data)
        food.goods_id = set3_uuid()
        food.shop_id = int(shop_id)
        db.session.add(food)
        db.session.commit()
        return redirect(url_for("cms.show_category", shop_id=shop.pub_id))
    return render_template("add_food.html", form=form)


# 菜品信息的展示
@cms_bp.route('/show_food/<shop_id>', endpoint='show_food', methods=['GET'])
@login_required
def show_category(shop_id):
    # 得到当前商铺对象
    shop = SellerShop.query.filter(SellerShop.id == shop_id).first()
    # 根据当前商铺查询菜品分类列表
    # 查询菜品MenuFood表中,shop_id全部为shop_id的菜品
    foods_list = MenuFood.query.filter(MenuFood.shop_id == shop_id).all()
    for x in foods_list:
        print(x.goods_name)
    return render_template("show_food.html", foods_list=foods_list)


# 菜品信息的修改
@cms_bp.route("/update_food/<food_id>", endpoint="update_food", methods=['GET', 'POST'])
@login_required
def update_food(food_id):
    # 根据菜品的id,进行查询
    food = MenuFood.query.filter(MenuFood.id == food_id).first()
    shop_id = food.shop_id
    food_pid = food.goods_id
    # shop = SellerShop.query.filter(SellerShop.id == shop_id).first()
    # shop_pid=shop.pub_id
    food_form = MenuFoodForm(request.form, shop_id=shop_id)
    # 将此对象字典话,放入MenuFoodForm中验证
    if request.method == "GET":
        food_form = MenuFoodForm(data=dict(food), shop_id=shop_id)
        return render_template("add_food.html", form=food_form)
    elif request.method == "POST":

        if form_to_model(food_form, food):
            # 添加shop_id
            return redirect(url_for("cms.show_food", shop_id=shop_id))
        else:
            return "修改失败"


# 写一个视图函数,用于菜品图片上传的时候,生成uptoken
@cms_bp.route("/generate_uptoken/", endpoint="generate_uptoken", methods=['GET', 'POST'])
@login_required
def generate_uptoken():
    AK = "sRA6m2inzA9sFRPDiDBh2gYoRU5SxsgevNq4i93W"
    SK = "5aBN29gQHFhmNeLwgR1bZOzYIwn-_0E44HMO840w"
    # 构建鉴权对象
    q = Auth(AK, SK)
    # 要上传的空间
    bucket_name = 'food-picture'
    token = q.upload_token(bucket=bucket_name)
    return jsonify({"uptoken": token})
