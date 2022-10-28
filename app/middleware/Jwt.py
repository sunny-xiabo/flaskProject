"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: Jwt.py
# @Date: 2022/9/27 13:14
"""

import hashlib
from datetime import datetime, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError

# 过期时间3小时
EXPIRED_HOUR = 3


class UserToken(object):
    """
        用户token工具类
    """
    key = 'cpityToken'
    salt = 'cpity'

    @staticmethod
    def get_token(data):
        """
        获取token
        :param data: 用户信息压缩成一串字符串，并附带3小时的过期时间
        :return:
        """
        new_data = dict({"exp": datetime.utcnow() + timedelta(hours=EXPIRED_HOUR)}, **data)
        return jwt.encode(new_data, key=UserToken.key)

    @staticmethod
    def parse_token(token):
        """
        解析token
        :param token:
        :return:  解析token为之前的用户信息
        """
        try:
            return jwt.decode(token, key=UserToken.key, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise Exception("Invalid token.")
        except Exception:
            raise Exception("Invalid token, Please login again. ")

    @staticmethod
    def add_salt(password):
        """
        加密密码
        :param password: md5 存储加密密码
        :return: 加密后的密码
        """
        m = hashlib.md5()
        bt = f"{password}{UserToken.salt}".encode("utf-8")
        m.update(bt)
        return m.hexdigest()
