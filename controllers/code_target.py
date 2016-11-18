#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/3/3

import datetime
import random
from time import time
from argeweb import auth, add_authorizations
from argeweb import Controller, scaffold, route_menu, Fields, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search
from ..models.code_target_model import CodeTargetModel
from ..models.code_model import CodeModel
from plugins.file.models.file_model import FileModel


class CodeTarget(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 10
        Model = FileModel

    class Scaffold:
        display_properties_in_list = ("title", "content_type", "last_version")

    @route_menu(list_name=u"backend", text=u"原始碼管理", sort=9713, group=u"檔案管理")
    def admin_list(self):
        model = self.meta.Model
        def query_factory_with_identifier(self):
            return model.code_files
        self.scaffold.query_factory = query_factory_with_identifier

        return scaffold.list(self)

    @route
    @route_menu(list_name=u"backend", text=u"線上編輯器", sort=9714, group=u"檔案管理")
    def admin_code_manager(self):
        self.context["list"] = self.meta.Model.code_files().fetch()
        for item in self.context["list"]:
            item.name = item.title.split("/")[-1]

    @route
    def admin_code_editor(self):
        self.context["target_id"] = self.params.get_string("key")
