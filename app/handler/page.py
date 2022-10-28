"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: page.py
# @Date: 2022/9/29 15:09
"""

from flask import request

# 默认页数和页码
PAGE = 1
SIZE = 10


class PageHandler(object):
    """
        分页类
    """

    @staticmethod
    def page():
        """
        获取page和size
        :return:
        """
        page = request.args.get('page')
        if page is None or not page.isdigit():
            page = PAGE
        size = request.args.get('size')
        if size is None or not size.isdigit():
            size = SIZE
        return int(page), int(size)
