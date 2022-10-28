"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: fatcory.py
# @Date: 2022/9/27 14:17
"""

'''
    转换orm对象为dict
    
'''

from datetime import datetime


class ResponseFactory(object):
    """
        转换orm 工具类
    """

    @staticmethod
    def model_to_dict(obj, *ignore: str):
        """
        实例转换为字典
        :param obj:
        :param ignore: 可变字符串参数
        :return:
        """
        data = dict()
        for c in obj.__table__.columns:
            if c.name in ignore:
                # 如果字段忽略，则不进行转换
                continue
            val = getattr(obj, c.name)
            # 针对datetime类对象做了特殊处理，这是因为JSON中没有对应的datetime格式，所以我们需要对它也进行转换
            if isinstance(val, datetime):
                data[c.name] = val.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[c.name] = val
        return data


    @staticmethod
    def model_to_list(data: list, *ignore: str):
        """
        列表生成
        :param data: orm 实例
        :param ignore: 可变字符串参数
        :return: list(orm object)
        """
        return [ResponseFactory.model_to_dict(x,*ignore) for x in data]
