"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: http.py
# @Date: 2022/9/28 15:25
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from app import cpity
from app.middleware.HttpClient import Request
from app.utils.decorator import permission

req = Blueprint('request', __name__, url_prefix='/request')


@req.route('/http', methods=['POST'])
@permission(cpity.config.get('ADMIN'))
def http_request(user_info):
    """
    封装http请求
    :return:
    """
    data = request.get_json()
    method = data.get('method')

    if not method:
        return jsonify(dict(code=101, msg='method is not empty'))

    url = data.get('url')
    if not url:
        return jsonify(dict(code=101, msg='url is not empty'))

    body = data.get('body')
    headers = data.get('headers')
    r = Request(url, data=body, headers=headers)
    response = r.request(method)
    if response.get('status'):
        return jsonify(dict(code=0, data=response, msg='success'))
    return jsonify(dict(code=110, data=response, msg=response.get('msg')))
