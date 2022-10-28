"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: HttpClient.py
# @Date: 2022/9/27 20:47
"""

import datetime
import requests


class Request(object):

    def __init__(self, url, session=False, **kwargs):
        self.url = url
        self.session = session
        self.kwargs = kwargs
        if self.session:
            self.client = requests.Session()
            return
        self.client = requests

    def get(self):
        return self.request('GET')

    @staticmethod
    def get_elapsed(timer: datetime.timedelta):
        """
        获取请求时间
        :param timer:
        :return: 请求时间大于1S以秒显示，请求时间小于1S以毫秒显示
        """
        if timer.seconds > 0:
            return f"{timer.seconds}.{timer.microseconds // 1000}s"
        return f"{timer.microseconds // 100}ms"

    def request(self, method: str):
        """

        :param method:
        :return:
        """
        status_code = 0
        elapsed = "-1ms"

        try:
            if method.upper() == 'GET':
                response = self.client.get(self.url, **self.kwargs)
            elif method.upper() == 'POST':
                response = self.client.post(self.url, **self.kwargs)
            else:
                response = self.client.request(method, self.url, **self.kwargs)
            status_code = response.status_code
            if status_code != 200:
                return Request.response(False, status_code)
            elapsed = Request.get_elapsed(response.elapsed)
            data = response.json()
            return Request.response(True, 200, data, response.headers, response.request.headers, elapsed=elapsed)

        except Exception as e:
            return Request.response(False, status_code, msg=str(e), elapsed=elapsed)

    def post(self):
        return self.request('POST')

    def get_response(self, response):
        try:
            return response.json()
        except:
            return response.text

    @staticmethod
    def response(status, status_code=200, response=None, response_headers=None,
                 request_headers=None, elapsed=None, msg="success"):
        request_headers = {k: v for k, v in request_headers.items()} if request_headers is not None else {}
        response_headers = {k: v for k, v in response_headers.items()} if response_headers is not None else {}
        return {
            "status": status, "response": response, "status_code": status_code,
            "response_header": response_headers, "request_header": request_headers,
            "msg": msg, "elapsed": elapsed,
        }
