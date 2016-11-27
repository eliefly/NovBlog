from flask import Blueprint

# 创建认证/管理蓝本
auth = Blueprint('auth', __name__)

# 关联蓝本和路由，生成映射。另一方式是使用app.add_url_rule()生成映射。
from . import views
