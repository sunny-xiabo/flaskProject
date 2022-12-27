"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: environment.py
# @Date: 2022/12/27 11:15
"""

from datetime import datetime
from sqlalchemy import INT, DATETIME, Column, String
from app.models import Base


class Environment(Base):
    "环境工具类"
    __tablename__ = 'cpity_environment'
    id = Column(INT, primary_key=True)
    # 环境名称
    name = Column(String, primary_key=True)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    created_user = Column(INT, nullable=True)
    updated_user = Column(INT, nullable=True)
    remarks = Column(String(200))


    def __init__(self, name, remarks, user, id=0):
        self.id = id
        self.created_user = user
        self.name = name
        self.remarks = remarks
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.updated_user = user