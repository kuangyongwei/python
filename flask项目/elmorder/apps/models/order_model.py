from apps.models import db, BaseModel


# 订单详情
class OrderInfo(BaseModel):
    order_code = db.Column(db.String(32), unique=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('seller_shop.pub_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('buyer_user.id'))
    # 订单送货地址
    order_address = db.Column(db.String(128))
    # 订单价钱
    order_price = db.Column(db.Float)
    # 订单状态
    order_status = db.Column(db.Integer)
    # 订单产生时间
    created_time = db.Column(db.DateTime, onupdate=True)
    # 第三方交易号
    trade_sn = db.Column(db.String(128))


# 订单的商品
class OrderGoods(BaseModel):
    order_id = db.Column(db.Integer, db.ForeignKey('order_info.id'))
    # 商品ID号
    goods_id = db.Column(db.Integer)
    # 商品名称
    goods_name = db.Column(db.String(64))
    # 商品图片
    goods_image = db.Column(db.String(128), default='')
    # 商品价钱
    goods_price = db.Column(db.Float)
    # 商品数量
    amount = db.Column(db.Integer)

    order = db.relationship('OrderInfo', backref='order_goods')
