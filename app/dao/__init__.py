"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: __init__.py.py
# @Date: 2022/9/27 11:05
"""

from app.models import db
from app.models.user import User
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.models.test_case import TestCase

db.create_all()