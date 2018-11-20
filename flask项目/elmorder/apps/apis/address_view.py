# 用户地址信息的添加管理
from flask import request, jsonify
from apps.apis import api_bp
from apps.forms.buyer_reg_form import AddAddressForm
from apps.models import db
from apps.models.buyer_model import BuyerAddressModel
from apps.pli import form_to_model
from apps.pli.token_validate import token_auth
from flask import g


# 添加地址
@api_bp.route('/add_address/', endpoint="add_address", methods=["POST"])
@token_auth
def add_address():
    form = AddAddressForm(request.form)
    if form.validate():
        add_address = BuyerAddressModel()
        add_address.set_attrs(form.data)
        add_address.user_id = g.current_user.id
        db.session.add(add_address)
        db.session.commit()
        return jsonify({"status": "true", "message": "添加地址成功"})
    return jsonify({"status": "false", "message": "添加地址失败"})


# 收货地址列表的展示
@api_bp.route('/address_list/', endpoint="address_list", methods=["GET"])
@token_auth
def address_list():
    addresses = g.current_user.addresses
    # print(user.id)
    # address = user.addresses
    data = [{**dict(x), "id": x.id} for x in addresses]
    return jsonify(data)


# 某个收货地址的展示
@api_bp.route('/address_up/', endpoint="address_up", methods=["GET"])
@token_auth
def address_up():
    id = request.args.get("id")
    # 得到收货地址的id,查询
    address = BuyerAddressModel.query.filter(BuyerAddressModel.id == id).first()
    data = {**dict(address), "id": id}
    return jsonify(data)


# 某个收货地址的修改
@api_bp.route('/edit_address/', endpoint="edit_address", methods=["POST"])
@token_auth
def edit_address():
    address = BuyerAddressModel.query.filter(BuyerAddressModel.id == request.form.get("id")).first()
    address_form = AddAddressForm(request.form)
    if address_form.validate() and form_to_model(address_form, address):
        # 数据合法,修改地址成功
        return jsonify({"status": "true", "message": "修改地址成功"})
    return jsonify({"status": "false", "message": "修改地址失败"})





    # add_id = request.form.get('id')
    # addre = BuyerAddressModel.query.filter_by(id=add_id)
    # address_form = AddAddressForm(request.form)
    # if address_form.validate():
    #     addre.set_attr(address_form.data)
    #     db.session.add(addre)
    #     db.session.commit()
    #     return jsonify({"status": "true", "message": "添加地址成功"})
    # return jsonify({"status": "false", "message": "添加地址失败"})
