"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: EnvironmentDao.py
# @Date: 2022/12/27 14:01
"""
from datetime import datetime

from sqlalchemy import desc

from app.models import Session
from app.models.environment import Environment
from app.models.schema.environment import EnvironmentForm
from app.utils.logger import Log
from app.utils.update_mod import update_model


class EnvironmentDao(object):
    log = Log("EnvironmentDao")

    @staticmethod
    def insert_env(data: EnvironmentForm, user):
        """
        新增环境
        :param data:
        :param user:
        :return:
        """
        try:
            # 从数据库拿到一个session，类似于db.cursor()也类似于jdbc里面的getConnection
            with Session() as session:
                query = session.query(Environment).filter_by(name=data.name, deleted_at=None).first()
                if query is not None:
                    return f"Environment{data.name}is existed."
                env = Environment(**data.dict(), user=user)
                session.add(env)
                session.commit()
        except Exception as e:
            EnvironmentDao.log.error(f"Insert Environment:{data.name} is failed, {e}")
            return f"Insert Environment{data.name} is failed,{str(e)}"
        return None

    @staticmethod
    def update_env(data: EnvironmentForm, user):
        """
        更新环境
        :param data:
        :param user:
        :return:
        """
        try:
            with Session() as session:
                query = session.query(Environment).filter_by(name=data.name, deleted_at=None).first()
                if query is not None:
                    return f"environment{data.name} does not exist"
                update_model(query, data, user)
                session.commit()
        except Exception as e:
            EnvironmentDao.log.error(f"Failed to update environment:{str(e)}")
            return f"Failed to update environment:{str(e)}"
        return None

    @staticmethod
    def delete_env(id, user):
        """
        删除环境（软删除）
        :param id:
        :param user:
        :return:
        """
        try:
            with Session() as session:
                query = session.query(Environment).filter_by(id=id).first()
                if query is None:
                    return f"environment{id} does not exist"
                query.deleted_at = datetime.now()
                query.update_user = user
                session.commit()
        except Exception as e:
            EnvironmentDao.log.error(f"Failed to delete environment:{str(e)}")
            return f"Failed to delete environment:{str(e)}"
        return None

    @staticmethod
    def list_env(page, size, name=None):
        """
        查询环境
        :param page:
        :param size:
        :param name:
        :return:
        """
        try:
            search = [Environment.deleted_at == None]
            with Session() as session:
                if name:
                    # 对name模糊查询
                    search.append(Environment.name.ilike("%{}%".format(name)))
                data = session.query(Environment).filter(*search)
                total = data.count()
                return data.order_by(desc(Environment.created_at)).offset((page - 1) * size).limit(
                    size).all(), total, None   # 自动分页
        except Exception as e:
            EnvironmentDao.log.error(f"Failed to obtain the environment list, {str(e)}")
            return [], 0, f"Failed to obtain the environment list, {str(e)}"
