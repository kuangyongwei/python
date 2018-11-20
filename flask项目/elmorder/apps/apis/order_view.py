from flask import request, g, jsonify

from apps.apis import api_bp
from apps.pli.token_validate import token_auth


@api_bp.route('/order_add/', endpoint="order_add", methods=["POST"])
@token_auth
def order_add():
    address_id = request.form.get("address_id")
    user = g.current_user
    # 根据用户,在redis中查询用户的购物车信息
    data = {
        "status": "true",
        "message": "添加成功",
        "order_id": 1
    }
    return jsonify(data)


# 获取订单列表
@api_bp.route('/orders_list/', endpoint="orders_list", methods=['GET'])
@token_auth
def orders_list():
    pass