#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import Controller, scaffold, route_menu, Fields, route_with
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search
from argeweb import BasicModel
from argeweb.behaviors.searchable import Searchable


def get_target(name):
    return CodeTargetModel.find_by_title(name)


class CodeTargetModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"Path",
            "content_type": u"ContentType",
            "last_version": u"Version",
        }
    title = Fields.StringProperty(default=u"未命名")
    content_type = Fields.StringProperty()
    last_version = Fields.IntegerProperty(default=0)

    @classmethod
    def content_type_sort_by_title(cls, content_type):
        """ get record with content-type and sort by title """
        return cls.query(cls.content_type == content_type).order(cls.title)

    @classmethod
    def before_delete(cls, key):
        from code_model import CodeModel
        CodeModel.delete_with_target(key)

