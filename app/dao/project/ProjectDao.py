"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: ProjectDao.py
# @Date: 2022/9/29 14:49
"""
from datetime import datetime

from sqlalchemy import or_

from app import cpity
from app.dao.project.ProjectRoleDao import ProjectRoleDao
from app.models import db
from app.models.project import Project
from app.utils.logger import Log


class ProjectDao(object):
    log = Log("ProjectDao")

    @staticmethod
    def list_project(user, role, page, size, name=None):
        """
        查询/获取项目列表
        :param user: 当前用户
        :param role: 当前用户角色
        :param page: 当前页码
        :param size: 当前size
        :param name: 项目名称
        :return:
        """
        try:
            search = [Project.deleted_at == None]
            if role != cpity.config.get('ADMIN'):
                project_list, err = ProjectRoleDao.list_project_by_user(user)
                if err is not None:
                    raise err
                search.append(or_(Project.id in project_list, Project.owner == user, Project.private == False))
            if name:
                search.append(Project.name.ilike("%{}%".format(name)))
            data = Project.query.filter(*search)
            total = data.count()
            return data.order_by(Project.created_at.desc()).paginate(page, per_page=size).items, total, None
        except Exception as e:
            ProjectDao.log.error(f"Get User: {user} list of projects failed,{e}")
            return [], 0, f"Get User: {user} list of projects failed,{e}"

    @staticmethod
    def add_project(name, app, owner, user, private, description):
        """
        增加项目
        :param name:
        :param owner:
        :param user:
        :param private:
        :return:
        """
        try:
            data = Project.query.filter_by(name=name, deleted_at=None).first()
            if data is not None:
                return "Project is already!!!"
            pr = Project(name, app, owner, user, description, private)
            db.session.add(pr)
            db.session.commit()
        except Exception as e:
            ProjectDao.log.error(f"Add Project: {name} Failed, {e}")
            return 0, 0, f"Add Project: {name} Failed, {e}"
        return None

    @staticmethod
    def query_project(project_id: int):
        try:
            data = Project.query.filter_by(id=project_id, deleted_at=None).first()
            # 数据为空判断
            if data is None:
                return None, [], "Project not found."
            # 权限判断
            roles, err = ProjectRoleDao.list_role(project_id)
            if err is not None:
                return None, [], err
            return data, roles, None
        except Exception as e:
            ProjectDao.log.error(f"Query Project: {project_id} failed, {e}")
            return None, [], f"Query Project: {project_id} Role list failed, {e}"

    @staticmethod
    def update_project(user, role, project_id, name,app, owner, private, description):
        """
        更新项目逻辑
        :param user:
        :param role:
        :param project_id:
        :param name:
        :param owner:
        :param private:
        :param description:
        :return:
        """
        try:
            data = Project.query.filter_by(id=project_id, deleted_at=None).first()
            if data is None:
                return "Project not found."
            data.name = name
            data.app = app
            # 判断修改人  不是本人或者超管
            if data.owner != owner and (role < cpity.config.get('ADMIN') or user != data.owner):
                return "You Don't have permission to edit this project leader."
            data.owner = owner
            data.private = private
            data.description = description
            data.updated_at = datetime.now()
            data.update_user = user
            db.session.commit()
        except Exception as e:
            ProjectDao.log.error(f"Edit Project: {name} Failed , {e}")
            return f"Edit Project: {name} Failed, {e}"
        return None
