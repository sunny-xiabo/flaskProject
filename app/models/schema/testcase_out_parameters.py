"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: testcase_out_parameters.py
# @Date: 2022/12/27 14:18
"""

from pydantic import BaseModel, validator

from app.models.schema.base import CPityModel


class CPityTestCaseOutParametersForm(BaseModel):
    id: int = None
    name: str
    expression: str = None
    match_index: str = None
    source: int

    @validator("name", "source")
    def name_not_empty(cls, v):
        return CPityModel.not_empty(v)
