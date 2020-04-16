# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)


class Config(object):
    """app配置相关信息类"""

    # SQLAlchemy相关配置选项
    # 设置连接数据库的URL
    # 注意：district_code数据库要事先手动创建
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qcl123@127.0.0.1:3306/xiao_long_xia'

    # 动态跟踪配置
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)


# 创建一个SQLAlchemy数据库连接对象
db = SQLAlchemy(app)

# 创建flask脚本管理工具对象
manager = Manager(app)

# 创建数据库迁移工具对象
Migrate(app, db)

# 向manager对象中添加数据库操作命令
manager.add_command("db", MigrateCommand)


class JDXlx(db.Model):
    """定义一个用来存储下龙虾数据的表"""
    # 定义表名
    __tblname__ = "jd_xlx"

    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String(32))  # 价格
    desc = db.Column(db.Text)  # 描述
    comments = db.Column(db.String(32))  # 评论数
    shop = db.Column(db.String(128))  # 店铺名称

    def __str__(self):
        return 'JDXlx:%s' % self.shop


if __name__ == '__main__':
    manager.run()

