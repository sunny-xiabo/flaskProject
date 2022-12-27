"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: environment.py
# @Date: 2022/12/27 12:02
"""

from pydantic import BaseModel, validator

from app.excpetions.ParamsException import ParamsError


class EnvironmentForm(BaseModel):
    id: int = None
    name: str
    remarks: str

    @validator("name")
    def name_not_empty(cls,v):
        if isinstance(v,str) and len(v.strip()) == 0:
            raise ParamsError("Can't be empty")
        return v
