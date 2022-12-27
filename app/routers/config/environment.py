"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: environment.py
# @Date: 2022/12/27 15:13
"""

from fastapi import APIRouter, Depends

from app.dao.config.EnvironmentDao import EnvironmentDao
from app.handler.fatcory import ResponseFactory
from app.models.schema.environment import EnvironmentForm
from app.routers import Permission
from config import Config

router = APIRouter(prefix="/config")


@router.get("/environment/list")
async def list_environment(page: int = 1, size: int = 8, name: str = "", user_info=Depends(Permission())):
    data, total, err = EnvironmentDao.list_env(page, size, name)
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, data=ResponseFactory.model_to_list(data), total=total, msg="Operations successfully")


@router.post("/environment/insert")
async def insert_environment(data: EnvironmentForm, user_info=Depends(Permission(Config.ADMIN))):
    err = EnvironmentDao.insert_env(data, user_info['id'])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, msg="Operations successfully")


@router.post("/environment/update")
async def update_environment(data: EnvironmentForm,user_info=Depends(Permission(Config.ADMIN))):
    err = EnvironmentDao.update_env(data,user_info['id'])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0,msg="Operations successfully")
