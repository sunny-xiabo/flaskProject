"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: project.py
# @Date: 2022/9/29 15:13
"""

from flask import Blueprint, request, jsonify

from app import cpity
from app.dao.project.ProjectRoleDao import ProjectRoleDao
from app.dao.project.ProjectDao import ProjectDao
from app.handler.fatcory import ResponseFactory
from app.handler.page import PageHandler
from app.utils.decorator import permission

pr = Blueprint("project", __name__, url_prefix="/project")


@pr.route("/list")
@permission()
def list_project(user_info):
    """
    获取项目列表
    :param user_info:
    :return:
    """

    page, size = PageHandler.page()
    user_role, user_id = user_info['role'], user_info['id']
    name = request.args.get('name')
    result, total, err = ProjectDao.list_project(user_id, user_role, page, size, name)
    if err is not None:
        return jsonify(dict(code=110, data=result, msg=err))
    return jsonify(dict(code=0, data=ResponseFactory.model_to_list(result), msg="Operation succeeded."))


@pr.route('/insert', methods=['POST'])
@permission(cpity.config.get('MANAGER'))
def insert_project(user_info):
    """
    增加项目
    :param user_info:
    :return:
    """
    try:
        user_id = user_info['id']
        data = request.get_json()
        if not data.get('name') or not data.get('owner'):
            return jsonify(dict(code=101, msg="Project name or Project owner Cannot be empty. "))
        if not data.get('app', ''):
            return jsonify(dict(code=101, msg="Service name cannot be empty. "))
        private = data.get('private', False)
        err = ProjectDao.add_project(data.get('name'), data.get('app'), data.get('owner'), user_id, private,
                                     data.get('description', ""))
        if err is not None:
            return jsonify(dict(code=110, msg=err))
        return jsonify(dict(code=0, msg="Operation succeeded."))
    except Exception as e:
        return jsonify(dict(code=111, msg=str(e)))


@pr.route("/query")
@permission()
def query_project(user_info):
    """
    项目详情接口
    :param user_info:
    :return:
    """
    project_id = request.args.get('projectId')
    if project_id is None or not project_id.isdigit():
        return jsonify(dict(code=101, msg="Please enter the correct project_id."))
    result = dict()
    data, roles, tree, err = ProjectDao.query_project(project_id)
    if err is not None:
        return jsonify(dict(code=110, data=result, msg=err))
    result.update({"project": ResponseFactory.model_to_dict(data), "roles": ResponseFactory.model_to_list(roles),
                   "test_case": tree})
    return jsonify(dict(code=0, data=result, msg="Operation succeeded."))


@pr.route("/update", methods=["POST"])
@permission()
def update_project(user_info):
    """
    修改项目信息接口
    :param user_info:
    :return:
    """
    try:
        user_id, role = user_info["id"], user_info["role"]
        data = request.get_json()
        if data.get('id') is None:
            return jsonify(dict(code=101, msg="Project id Cannot be empty."))
        if not data.get('name') or not data.get('owner'):
            return jsonify(dict(code=101, msg="Project name or Project leader Cannot be empty."))
        if not data.get('app', ''):
            return jsonify(dict(code=101, msg="Service name Cannot be empty."))
        private = data.get('private', False)
        err = ProjectDao.update_project(user_id, role, data.get('id'), data.get('app'), data.get("name"),
                                        data.get("owner"), private,
                                        data.get("description", ""))
        if err is not None:
            return jsonify(dict(code=110, msg=err))
        return jsonify(dict(code=0, msg="Operation succeeded."))
    except Exception as e:
        return jsonify(dict(code=111, msg=str(e)))


@pr.route("/role/insert", methods=["POST"])
@permission()
def insert_project_role(user_info):
    """
    新增权限接口
    :param user_info:
    :return:
    """
    try:
        data = request.get_json()
        if data.get("user_id") is None or data.get("project_role") is None or data.get("project_id") is None:
            return jsonify(dict(code=101, msg="Wrong request parameters!!!"))
        err = ProjectRoleDao.add_project_role(data.get("user_id"), data.get("project_id"), data.get("project_role"),
                                              user_info["id"])
        if err is not None:
            return jsonify(dict(code=110, msg=err))

    except Exception as e:
        return jsonify(dict(code=110, msg=str(e)))
    return jsonify(dict(code=0, msg="Operation succeeded."))


@pr.route("/role/update", methods=["POST"])
@permission()
def update_project_role(user_info):
    try:
        data = request.get_json()
        if data.get("user_id") is None or data.get("project_role") is None or data.get("project_id") is None \
                or data.get("id") is None:
            return jsonify(dict(code=101, msg="Wrong request parameters!!!"))
        err = ProjectRoleDao.update_project_role(data.get("id"), data.get("project_role"),
                                                 user_info["id"], user_info["role"])
        if err is not None:
            return jsonify(dict(code=110, msg=err))
    except Exception as e:
        return jsonify(dict(code=110, msg=str(e)))
    return jsonify(dict(code=0, msg="Operation succeeded."))
