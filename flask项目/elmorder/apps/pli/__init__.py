import uuid

from redis import Redis

from apps.models import db


# 生成14位uuid字符串,商家店铺用

def set1_uuid():
    b = str(uuid.uuid4()).rsplit("-", maxsplit=1)
    return b[1]


# 菜单分类用
def set2_uuid():
    b = str(uuid.uuid4()).split("-")
    return b[4] + b[3]


# 菜品信息用
def set3_uuid():
    b = str(uuid.uuid4()).split("-")
    return b[4] + b[2]


# 把form元素的内容更新到数据模型
def form_to_model(form, model):
    if form.validate():
        for k, v in form.data.items():
            if hasattr(model, k):
                setattr(model, k, v)
        db.session.add(model)
        db.session.commit()
        return True


api_redis = Redis('192.168.205.129', port=6388, db=1)
