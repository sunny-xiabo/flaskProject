"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: config.py
# @Date: 2022/9/26 19:51
"""

# 基础配置类
import os


class Config(object):
    ROOT = os.path.dirname(os.path.abspath(__file__))
    LOG_NAME = os.path.join(ROOT, 'logs', 'cpity.log')
    JSON_AS_ASCII = False  # JSON_AS_ASCII 解决flask jsonify 编码问题

    # mysql连接信息
    MYSQL_HOST = "124.223.178.186"
    MYSQL_PORT = "3307"
    MYSQL_USER = "root"
    MYSQL_PWD = "xiabo666"
    DBNAME = "cpity"

    # 设置数据库连接地址
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
        MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, DBNAME)
    # 是否追踪数据库修改(开启后会触发一些钩子函数)  一般不开启, 会影响性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否显示底层执行的SQL语句
    # SQLALCHEMY_ECHO = True


    # 权限 0 普通用户 1 组长 2 管理员
    MEMBER = 0
    MANAGER = 1
    ADMIN = 2

