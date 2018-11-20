import json

from apps.apis import api_bp
from apps.models.food_model import MenuFood
from apps.pli import api_redis
from apps.pli.token_validate import token_auth
from flask import g, request, current_app, jsonify


def check_cart_state(cart_key):
    result = api_redis.hgetall(cart_key)
    if result:
        # 说明redis里有数据，那么清空该条记录
        api_redis.delete(cart_key)


@api_bp.route('/save_cart/', endpoint="save_cart", methods=["POST"])
@token_auth
def save_cart():
    # 得到页面提交过来的数据
    user = g.current_user
    good_pid_list = request.form.getlist("goodsList[]")
    good_cont = request.form.getlist("goodsCount[]")
    # 得到当前用户,得到购物车中需要保存的商品对外id,商品数量列表
    if len(good_pid_list) and len(good_cont):
        cart_key = "cart_{}".format(user.id)
        check_cart_state(cart_key)
        for good_pid, cont in zip(good_pid_list, good_cont):
            food = MenuFood.query.filter(MenuFood.goods_id == good_pid).first()
            food_info = {
                "amount": cont,
                "goods_name": food.goods_name,
                "goods_price": food.goods_price,
                "goods_img": food.goods_img
            }
            # 将当前用户的购物车数据保存以hash形式到redis中
            api_redis.hset(cart_key, good_pid, json.dumps(food_info))
            # 设置数据的过期时间
        api_redis.expire(cart_key, current_app.config.get("CART_LIFETIME", 3600))
        return jsonify({"status": "true", "message": "添加成功"})
    else:
        return jsonify({'status': 'false', 'message': '没有选着菜品来添加'})


# 显示购买的数据
@api_bp.route('/cart/', endpoint="cart", methods=["GET"])
@token_auth
def cart():
    # 得到当前买家对象
    user = g.current_user
    cart_key = "cart_{}".format(user.id)
    goods = api_redis.hgetall(cart_key)
    total = 0
    good_list = []
    for key, value in goods.items():
        good_info = json.loads(value)
        good_list.append(good_info)
        total += int(good_info["amount"]) * good_info["goods_price"]

    return jsonify({'goods_list': good_list, "totalCost": total})
