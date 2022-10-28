"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: __init__.py.py
# @Date: 2022/9/27 10:40
"""

from flask_sqlalchemy import SQLAlchemy

from app import cpity

db = SQLAlchemy(cpity)
