"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: executor.py
# @Date: 2022/10/28 23:43
"""

import json

from app.dao.test_case.TestCaseDao import TestCaseDao
from app.middleware.HttpClient import Request
from app.utils.logger import Log


class Executor(object):
    """
        执行用例工具类
    """
    log = Log("executor")

    @staticmethod
    def run(case_id: int):
        """
        执行方法
        :param case_id:
        :return:
        """
        result = dict()
        try:
            case_info, err = TestCaseDao.query_test_case(case_id)
            if err:
                return result, err
                # 说明取到了用例数据
            if case_info.request_header != "":
                headers = json.loads(case_info.request_header)
            else:
                headers = dict()
            if case_info.body != '':
                body = case_info.body
            else:
                body = None
            request_obj = Request(case_info.url, headers=headers, data=body)
            method = case_info.request_method.upper()
            response_info = request_obj.request(method)
            return response_info, None
        except Exception as e:
            Executor.log.error(f"Failed to execute case: {str(e)}")
            return result, f"Failed to execute case: {str(e)}"
