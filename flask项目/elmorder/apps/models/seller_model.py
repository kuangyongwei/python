from apps.models import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from apps import login_manager


# 用户登录信息表
class SellerLoginModel(BaseModel, UserMixin):
    seller_phone = db.Column(db.String(11), unique=True, nullable=False)
    _password = db.Column("password", db.String(128), )

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, val):
        self._password = generate_password_hash(val)

    def check_password(self, in_password):
        return check_password_hash(self.password, in_password)

    def __repr__(self):
        return "<SellerLoginModel : {}>".format(self.seller_phone)


@login_manager.user_loader
def load_user(user_id):
    return SellerLoginModel.query.get(int(user_id))
