"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: ProjectRoleDao.py
# @Date: 2022/9/29 14:37
"""
from datetime import datetime

from app import cpity
from app.models import db
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.utils.logger import Log


class ProjectRoleDao(object):
    log = Log("ProjectRoleDao")

    @staticmethod
    def list_project_by_user(user_id):
        """
        通过user_id 获取项目列表
        :param user_id:
        :return:
        """
        try:
            projects = ProjectRole.query.filter_by(user_id=user_id, deleted_at=None).all()
            return [p.id for p in projects], None
        except Exception as e:
            ProjectRoleDao.log.error(f"check user: {user_id} project failed, {e}")
            return [], f"Failed to list project,{e}"

    @staticmethod
    def add_project_role(user_id, project_id, project_role, user):
        """
        为项目添加用户
        :param user_id: 用户id
        :param project_id: 项目id
        :param project_role: 用户角色
        :param user: 创建人
        :return:
        """
        try:
            role = ProjectRole.query.filter_by(user_id=user_id, project_id=project_id, project_role=project_role,
                                               deleted_at=None).first()
            if role is not None:
                # 说明角色已经存在了
                return "This user  is already"
            role = ProjectRole(user_id, project_id, project_role, user)
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            ProjectRoleDao.log.error(f"Failed to add project user, {e}")
            return f"Failed to add project user, {e}"
        return None

    @staticmethod
    def list_role(project_id: int):
        try:
            roles = ProjectRole.query.filter_by(project_id=project_id, deleted_at=None).all()
            return roles, None
        except Exception as e:
            ProjectRoleDao.log.error(f"Query Project: {project_id} Role list failed, {e}")
            return [], f"Query Project: {project_id} Role list failed, {e}"

    @staticmethod
    def update_project_role(role_id: int, project_role, user, user_role):
        """
        修改用户信息逻辑
            `判断他要修改的角色id是否存在
            `判断是否是超管或者owner
            `判断要修改的是不是组长
            `判断他自身是否是组长
        :param role_id:
        :param project_role:
        :param user:
        :param user_role:
        :return:
        """
        try:
            role = ProjectRole.query.filter_by(id=role_id, deleted_at=None).first()
            if role is None:
                return "This User role does not exist."
            if user_role != cpity.config.get('ADMIN'):
                project = Project.query.filter_by(id=role.project_id).first()
                if project is None:
                    return "This Project does not exist."
                if project.owner != user and role.project_role == 1:
                    # 说明既不是owner也不是超管，无法修改组织的权限
                    return "The Authority of the other Group leaders cannot be modified."
            updater_role = ProjectRole.query.filter_by(user_id=user, project_id=role.project_id,
                                                       deleted_at=None).first()
            if updater_role is None or updater_role.project_role == 1:
                return "Sorry, You don't have permission to modify this project."
            role.project_role = project_role
            role.updated_at = datetime.now()
            role.update_user = user
            db.session.commit()

        except Exception as e:
            ProjectRoleDao.log.error(f"Edit Project User Failed,{e}")
            return f"Edit Project User Failed, {e}"
        return None

    @staticmethod
    def delete_project_role(role_id, user, user_role):
        """

        :param role_id:
        :param user:
        :param user_role:
        :return:
        """
        try:
            role = ProjectRole.query.filter_by(id=role_id, deleted_at=None).first()
            if role is None:
                return "User role does not exist."
            err = ProjectRoleDao.has_permission(role.project_id, role.project_role, user, user_role, True)
            if err is not None:
                return err
            role.updated_at = datetime.now()
            role.deleted_at = datetime.now()
            role.deleted_at = datetime.now()
            db.session.commit()
        except Exception as e:
            ProjectRoleDao.log.error(f"Delete Project User Failed,{e}")
            return f"Delete Project User Failed, {e}"

    @staticmethod
    def has_permission(project_id, project_role, user, user_role, project_admin=False):
        """

        :param project_id:
        :param project_role:
        :param user:
        :param user_role:
        :param project_admin:
        :return:
        """
        if user_role != cpity.config.get('ADMIN'):
            project = Project.query.filter_by(id=project_id).first()
            if project is None:
                return "This project does not exist."
            if project.owner != user:
                if project_admin and project_role == 1:
                    return "The team leader's authority cannot be modified"
                updater_role = ProjectRole.query.filter_by(user_id=user, project_id=project_id, deleted_at=None).first()
                if updater_role is None or updater_role.project_role == 0:
                    return "Sorry, you don't have permission."

        return None
