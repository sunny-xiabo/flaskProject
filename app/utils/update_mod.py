"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: update_mod.py
# @Date: 2022/12/27 14:39
"""

from datetime import datetime


def update_model(dist, source, update_user=None, not_null=False):
    """

    :param dist: 被修改的参数
    :param source: Pydantic的BaseModel,也就是web页面的表单数据
    :param update_user: 每条数据都带有updated_at,update_user信息，在update的时候自动设置当前时间
    :param not_null: 可选参数，如果是True,那么只有非空字段会被更新
    :return:
    """

    for var, value in vars(source).items():
        if not_null:
            if value:
                setattr(dist, var, value)
        else:
            setattr(dist, var, value)
        if update_user:
            setattr(dist, 'update_user', update_user)
        setattr(dist, 'updated_at',datetime.now())
