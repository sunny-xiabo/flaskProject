"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: user.py
# @Date: 2022/9/26 20:24
"""

from flask import Blueprint, request
from flask import jsonify

from app.dao.auth.UserDao import UserDao
from app.handler.fatcory import ResponseFactory
from app.middleware.Jwt import UserToken
from app.utils.decorator import permission

auth = Blueprint('auth', __name__, url_prefix='/auth')


# 这里以auth.route 注册的函数都会自带 /auth, 所以url 是/auth/register
@auth.route('/register', methods=['POST'])
def register():
    """
    注册接口
    :return:
    """
    # 获取request 请求数据
    data = request.get_json()
    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return jsonify(dict(code=101, msg='username or password cannot be empty'))

    email, name = data.get('email'), data.get('name')
    if not email or not name:
        return jsonify(dict(code=101, msg='email or name cannot be empty'))

    err = UserDao.register_user(username, name, password, email)
    if err is not None:
        return jsonify(dict(code=110, msg=err))
    return jsonify(dict(status=0, msg="注册成功"))


@auth.route('/login', methods=['POST'])
def login():
    """
    登录接口
    :return:
    """
    data = request.get_json()
    username, password = data.get('username'), data.get('password')
    if not username or not password:
        return jsonify(dict(code=101, msg='username or password cannot be empty'))

    user, err = UserDao.login(username, password)
    if err is not None:
        return jsonify(dict(code=110, msg=err))
    # 隐藏用户的password
    user = ResponseFactory.model_to_dict(user, "password")
    token = UserToken.get_token(user)
    if err is not None:
        return jsonify(dict(code=110, msg=err))
    return jsonify(dict(code=0, msg="login successfully", data=dict(token=token, user=user)))


@auth.route('/listUser')
@permission()
def list_users(user_info):
    """
    用户列表接口
    :param user_info:
    :return:
    """
    users, err = UserDao.list_users()
    if err is not None:
        return jsonify(dict(code=110, msg=err))
    return jsonify(dict(code=0, msg="Operation succeeded.", data=ResponseFactory.model_to_list(users)))
