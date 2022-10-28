"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: testcase.py
# @Date: 2022/10/28 17:42
"""
from flask import request, Blueprint, jsonify

from app.dao.test_case.TestCaseDao import TestCaseDao
from app.handler.fatcory import ResponseFactory
from app.utils.decorator import permission, json_validate

ts = Blueprint("testcase", __name__, url_prefix="/testcase")

# test case 数据
testcase = {"type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                },
                "name": {
                    "type": "string",
                },
                "request_type": {
                    "type": "integer",
                },
                "url": {
                    "type": "string",
                },
                "request_method": {
                    "type": "string",
                },
                "request_header": {
                    "type": "string",
                },
                "params": {
                    "type": "string",
                },
                "body": {
                    "type": "string",
                },
                "project_id": {
                    "type": "integer",
                },
                "tag": {
                    "type": "string",
                },
                "status": {
                    "type": "integer",
                },
                "priority": {
                    "type": "string",
                },
                "catalogue": {
                    "type": "string",
                },
                "expected": {
                    "type": "string",
                },
            },
            "required": ["expected", "catalogue", "priority", "status", "project_id", "request_type", "url", "name"]
            }


@ts.route('/insert', methods=['POST'])
@json_validate(testcase)  # 校验JSON parameters
@permission()
def insert_testcase(user_info):
    """
    添加用例接口
    :param user_info:
    :return:
    """
    data = request.get_json()
    err = TestCaseDao.insert_test_case(data, user_info['id'])
    if err:
        return jsonify(dict(code=110, msg=err))
    return jsonify(dict(code=0, msg="Operation succeeded."))


@ts.route('/query')
@permission()
def query_testcase(user_info):
    """
    查询用例
    :param user_info:
    :return:
    """
    case_id = request.args.get('caseId')
    if case_id is None or not case_id.isdigit():  # isdigit 检测字符串是否只由数字组成，只对 0 和 正数有效
        return jsonify(dict(code=101, msg="Incorrect caseId."))
    data, err = TestCaseDao.query_test_case(int(case_id))
    if err:
        return jsonify(dict(code=110, msg=err))
    return jsonify(dict(code=0, data=ResponseFactory.model_to_dict(data), msg="Operation succeeded."))
