"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: decorator.py
# @Date: 2022/9/26 20:15
"""

from functools import wraps
from flask import request, jsonify
from app import cpity
from app.middleware.Jwt import UserToken
from jsonschema import validate, FormatChecker, ValidationError

FORBIDDEN = "Sorry, you don't have enough permissions!"


class SingletonDecorator:
    """
    装饰器方法
    首先判断该类的实例是否是None，为None的话则生成新实例，否则返回该实例。这样就确保了只生成一次实例
    """

    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


def permission(role=cpity.config.get('MEMBER')):
    def login_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                headers = request.headers
                token = headers.get('token')
                if token is None:
                    return jsonify(dict(code=401, msg='Invalid token, please check your token validity'))
                user_info = UserToken.parse_token(token)
                # user信息写入kwargs
                kwargs["user_info"] = user_info
            except Exception as e:
                return jsonify(dict(code=401, msg=str(e)))

            # 判断用户权限是否足够，如果不足够则直接返回，不继续
            if user_info.get("role", 0) < role:
                return jsonify(dict(code=400, msg=FORBIDDEN))
            return func(*args, **kwargs)

        return wrapper

    return login_required


def json_validate(sc):
    """
    校验json数据
    :param sc:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request.get_json() is not None:
                    validate(request.get_json(), sc, format_checker=FormatChecker())
                else:
                    raise Exception("The request json parameter is illegal.")
            except ValidationError as e:
                return jsonify(dict(code=101, msg=str(e.message)))  # 返回参数校验失败信息
            except Exception as e:
                return jsonify(dict(code=101, msg=str(e)))
            return func(*args, **kwargs)

        return wrapper

    return decorator
