from flask import Blueprint

# 创建蓝本
main = Blueprint('main', __name__)

# 关联蓝本和路由，放在末尾为了避免循环导入的依赖，因为在views中还要导入蓝本main
from . import views
