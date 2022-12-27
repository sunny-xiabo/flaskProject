"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: base.py
# @Date: 2022/12/27 14:23
"""

from app.excpetions.ParamsException import ParamsError


class CPityModel(object):

    @staticmethod
    def not_empty(v):
        if isinstance(v,str) and len(v.strip()) == 0:
            raise ParamsError("Can't be empty")
        if not isinstance(v,int):
            if not v:
                raise ParamsError("Can't be empty")
        return v

    @property
    def parameters(self):
        raise NotImplementedError
