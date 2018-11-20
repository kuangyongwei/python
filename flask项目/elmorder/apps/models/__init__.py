from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    '''
    抽象类,如果不加上__abstract__,会将后面继承该类的模型都建立到一张表里面
    '''
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def set_attrs(self, attrs):
        for k, v in attrs.items():
            # id必须为字符串
            if hasattr(self, k) and k != "id":
                setattr(self, k, v)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)


from . import seller_model
from . import shop_model
from . import food_model
from . import buyer_model
from . import order_model