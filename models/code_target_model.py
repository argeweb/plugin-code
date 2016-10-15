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
import logging


def get_by_name(name):
    return CodeTargetModel.get_by_name(name)


class CodeTargetModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"目標名稱",
            "content_type": u"ContentType",
            "last_version": u"Version",
        }
    title = Fields.StringProperty(default=u"未命名")
    content_type = Fields.StringProperty()
    last_version = Fields.IntegerProperty(default=0)

    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.title==name).get()

    @classmethod
    def content_type_sort_by_title(cls, content_type):
        """
        Queries all posts in the system, regardless of user, ordered by date created descending.
        """
        return cls.query(cls.content_type == content_type).order(cls.title)
