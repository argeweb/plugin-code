#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import BasicModel
from argeweb.behaviors.searchable import Searchable
from argeweb import Fields
from code_target_model import CodeTargetModel


def get_source(target, code_type, version=None):
    return CodeModel.get_source(target, code_type, version)


class CodeModel(BasicModel):
    class Meta:
        behaviors = (Searchable,)
        label_name = {
            "title": u"團體名稱",
            "customer": u"所屬客戶",
            "content_type": u"類型",
            "source": u"原始碼",
        }
    title = Fields.StringProperty(default=u"未命名")
    target = Fields.CategoryProperty(kind=CodeTargetModel)
    content_type = Fields.StringProperty()
    source = Fields.TextProperty()
    source_mini = Fields.TextProperty()
    version = Fields.IntegerProperty(default=0)

    @classmethod
    def all_with_target(cls, target, content_type):
        return cls.query(cls.content_type == content_type, cls.target == target.key).order(-cls.sort)

    @classmethod
    def get_source(cls, target, content_type, version=None):
        if version is not None:
            return cls.query(cls.content_type == content_type, cls.target == target.key, cls.version == int(version)).order(-cls.sort).get()
        else:
            return cls.query(cls.content_type == content_type, cls.target == target.key).order(-cls.version).get()
