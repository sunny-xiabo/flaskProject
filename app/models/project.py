"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: project.py
# @Date: 2022/9/29 13:47
"""

from app.models import db
from datetime import datetime


class Project(db.Model):
    """
        项目表
    """
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(16), unique=True, index=True)  # 项目名
    owner = db.Column(db.INT)  # 组长
    app = db.Column(db.String(32), index=True)
    created_at = db.Column(db.DATETIME, nullable=False)
    updated_at = db.Column(db.DATETIME, nullable=False)
    deleted_at = db.Column(db.DATETIME)
    create_user = db.Column(db.INT, nullable=True)
    update_user = db.Column(db.INT, nullable=True)
    private = db.Column(db.BOOLEAN, default=False)  # 是否私有
    description = db.Column(db.String(255))

    def __init__(self, name, app, owner, create_user, description="", private=False):
        self.name = name
        self.app = app
        self.owner = owner
        self.private = private
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.created_user = create_user
        self.update_user = create_user
        self.description = description
        self.deleted_at = None
