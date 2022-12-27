"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: RequestException.py
# @Date: 2022/12/27 15:49
"""

from fastapi import HTTPException


class AuthException(HTTPException):
    pass


class PermissionException(HTTPException):
    pass
