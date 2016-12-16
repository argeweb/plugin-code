#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import BasicModel
from argeweb import Fields
from plugins.file.models.file_model import FileModel
from google.appengine.ext import ndb


def get_source(target, version=None):
    return CodeModel.get_source(target, version)


class CodeModel(BasicModel):
    title = Fields.StringProperty(default=u'未命名')
    target = Fields.CategoryProperty(kind=FileModel)
    content_type = Fields.StringProperty()
    source = Fields.TextProperty()
    source_mini = Fields.TextProperty()
    version = Fields.IntegerProperty(default=0)

    @classmethod
    def all_with_target(cls, target, content_type):
        return cls.query(cls.content_type == content_type, cls.target == target.key).order(-cls.sort)

    @classmethod
    def get_source(cls, target, version=None):
        if version is not None and version != "":
            return cls.query(cls.target == target.key, cls.version == int(version)).order(-cls.sort).get()
        else:
            return cls.query(cls.target == target.key).order(-cls.version).get()

    @classmethod
    def delete_with_target(cls, target_key):
        multi_keys = cls.query(cls.target == target_key).fetch(keys_only=True)
        ndb.delete_multi(multi_keys)
