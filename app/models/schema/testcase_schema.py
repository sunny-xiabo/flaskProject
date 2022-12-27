"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: testcase_schema.py
# @Date: 2022/12/27 14:15
"""
from typing import List

from pydantic import BaseModel, validator

from app.excpetions.ParamsException import ParamsError
from app.models.schema.testcase_out_parameters import CPityTestCaseOutParametersForm


class TestCaseForm(BaseModel):
    id: int = None
    priority: str
    url: str = ""
    name: str = ""
    case_type: int = 0
    base_path: str = None
    tag: str = None
    body: str = None
    body_type: int = 0
    request_headers: str = None
    request_method: str = None
    status: int
    out_parameters: List[CPityTestCaseOutParametersForm] = []
    directory_id: int
    request_type: int

    @validator("priority", "status", "directory_id", "request_type", "url", "name")
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("Cannot be empty")
        return v