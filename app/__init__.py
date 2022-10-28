"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: __init__.py.py
# @Date: 2022/9/26 19:45
"""

from flask import Flask
from config import Config
from flask_cors import CORS


cpity = Flask(__name__)
# 解决跨域问题
CORS(cpity, supports_credentials=True)

cpity.config.from_object(Config)




