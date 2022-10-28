"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: project_role.py
# @Date: 2022/9/29 13:57
"""

from app.models import db
from datetime import datetime


class ProjectRole(db.Model):
    """
        项目角色表
    """
    id = db.Column(db.INT, primary_key=True)
    project_id = db.Column(db.INT, index=True)
    project_role = db.Column(db.INT, index=True)  # 项目角色
    created_at = db.Column(db.DATETIME, nullable=False)
    updated_at = db.Column(db.DATETIME, nullable=False)
    deleted_at = db.Column(db.DATETIME)
    create_user = db.Column(db.INT, nullable=True)
    update_user = db.Column(db.INT, nullable=True)

    def __init__(self, project_id, project_role, create_user):
        self.project_id = project_id
        self.project_role = project_role
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = create_user
        self.update_user = create_user
        self.deleted_at = None
