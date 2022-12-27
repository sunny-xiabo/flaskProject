"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: __init__.py.py
# @Date: 2022/12/27 15:11
"""
from fastapi import Header
from starlette import status

from app.dao.auth import UserDao
from app.excpetions.RequestException import AuthException, PermissionException
from app.handler.fatcory import ResponseFactory
from app.middleware.Jwt import UserToken
from app.models import async_session
from config import Config

FORBIDDEN = "Sorry,You don't have enough access"

class Permission:

    def __init__(self,role:int= Config.MEMBER):
        self.role = role

    async def __call__(self, token:str=Header(...)):
        if not token:
            raise AuthException(status.HTTP_200_OK,"User information identity authentication failed. Please check")
        try:
            user_info = UserToken.parse_token(token)
            if user_info.get("role", 0) < self.role:
                raise PermissionException(status.HTTP_200_OK, FORBIDDEN)
            user = await UserDao.query_user(user_info['id'])
            if user is None:
                raise Exception("用户不存在")
            user_info = ResponseFactory.model_to_dict(user, "password")
        except PermissionException as e:
            raise e
        except Exception as e:
            raise AuthException(status.HTTP_200_OK, str(e))
        return user_info

async def get_session():
    """
    获取异步session
    :return:
    """
    async with async_session() as session:
        yield session