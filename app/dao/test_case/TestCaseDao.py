"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: TestCaseDao.py
# @Date: 2022/9/30 15:43
"""
from app.models import db
from app.models.test_case import TestCase
from app.utils.logger import Log

from collections import defaultdict


class TestCaseDao(object):
    log = Log("TestCaseDao")

    @staticmethod
    def list_test_case(project_id):
        try:
            case_list = TestCase.query.filter_by(project_id=project_id, deleted_at=None).order_by(
                TestCase.name.asc()).all()
            return TestCaseDao.get_tree(case_list), None
        except Exception as e:
            TestCaseDao.log.error(f"Failed to list test cases: {str(e)}")
            return [], f"Failed to list test cases: {str(e)}"

    @staticmethod
    def get_tree(case_list):
        result = defaultdict(list)
        # 获取目录 -> 用例的映射关系
        for cs in case_list:
            result[cs.catalogue].append(cs)
        keys = sorted(result.keys())
        tree = [dict(key=f"cat_{key}",
                     children=[{"key": f"case_{child.id}", "title": child.name} for child in result[key]],
                     title=key, total=len(result[key])) for key in keys]
        return tree

    @staticmethod
    def insert_test_case(test_case, user):
        """
        新增用例
        :param test_case: 测试用例
        :param user: 创建人
        :return:
        """
        try:
            # 通过name 和 project_id 过滤查询
            data = TestCase.query.filter_by(name=test_case.get('name'), project_id=test_case.get('project_id'),
                                            deleted_at=None).first()
            if data is not None:
                return "testcase is already inserted."
            cs = TestCase(**test_case, create_user=user)
            db.session.add(cs)
            db.session.commit()
        except Exception as e:
            TestCaseDao.log.error(f"insert testcase failed:{str(e)}")
            return f"insert testcase failed: {str(e)}"
        return None

    @staticmethod
    def query_test_case(case_id):
        """
        根据用例id获取用例信息
        :param case_id: 用例ID
        :return: 用例信息
        """
        try:
            data = TestCase.query.filter_by(id=case_id, deleted_at=None).first()
            if data is None:
                return None, "TestCase not be empty."
            return data, None
        except Exception as e:
            TestCaseDao.log.error(f"Failed to query testcase: {str(e)}")
            return None, f"Failed to query testcase: {str(e)}"
