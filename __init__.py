#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
import webapp2
from google.appengine.ext import webapp
from argeweb.core import settings

plugins_helper = {
    "title": u"線上編輯原始碼",
    "desc": u"可以以動態的方式進行程式碼編輯",
    "controllers": {
        "code": {
            "group": u"原始碼",
            "actions": [
                {"action": "code_manager", "name": u"線上編輯器"},
                {"action": "code_editor", "name": u"編輯"},
                {"action": "list", "name": u"原始碼管理"},
                {"action": "add", "name": u"新增原始碼"},
                {"action": "edit", "name": u"編輯原始碼"},
                {"action": "view", "name": u"檢視原始碼"},
                {"action": "delete", "name": u"刪除原始碼"},
            ]
        }
    }
}


def get_params_from_file_name(target_name, hotfix):
    is_min = False
    if str(target_name).endswith(".min"):
        is_min = True
        target_name = target_name.split(".min")[0]
    try:
        version = target_name.split("/")[-1].split("_")[-1].split(".")[0]
        version = int(version)
        target_name = target_name.split("_"+str(version))[0]
    except:
        version = ""
    target_name = "/" + target_name + "." + hotfix
    content_type = "javascript" if hotfix == "js" else "css"
    return target_name, str(version), is_min, content_type


class GetFileHandler(webapp2.RequestHandler):
    def get(self, target_name):
        content_type = None
        c = target_name.startswith("/code") and "code" or "assets"
        if target_name.endswith(".js"):
            content_type = "js"
        if target_name.endswith(".css"):
            content_type = "css"
        target_name = target_name.replace("/" + c, "").replace("." + content_type, "")
        from plugins.file.models.file_model import FileModel
        from google.appengine.api import namespace_manager
        if content_type is None:
            content_type, target_name, c = target_name, c, "assets"

        host_information, namespace, theme = settings.get_host_information_item()
        namespace_manager.set_namespace(namespace)
        target_name, version, is_min, content_type = get_params_from_file_name(target_name, content_type)
        if target_name.startswith(u"/themes/%s" % theme) is False:
            target_name = u"/themes/%s%s" % (theme, target_name)
        if self.request.headers.get('If-None-Match'):
            match = self.request.headers.get('If-None-Match').split("||")
            if u"" + match[0] == target_name and u"" + match[-1] == theme:
                return self.abort(304)
        c = FileModel.get_by_path(target_name)
        if c is None:
            return self.abort(404)
        version = str(c.last_version) if version is "" else version
        etag = str(target_name) + "||" + version + "||" + str(theme)
        if self.request.headers.get('If-None-Match') == etag:
            return self.abort(304)
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        self.response.headers["Cache-control"] = "public, max-age=60" if version is "" else "public, max-age=604800"
        self.response.headers['Content-Type'] = 'text/' + content_type
        self.response.headers["ETag"] = etag
        from models.code_model import CodeModel
        s = CodeModel.get_source(target=c, content_type=content_type, version=version)
        if s is None:
            return self.abort(404)
        if is_min is True:
            source = s.source_mini
        else:
            source = s.source
        self.response.out.write(source)
        # self.meta.change_view('render')
        # self.meta.view.template_name = "code/" + content_type + ".html"
        # self.context["record"] = {
        #     "target_name": target_name,
        #     "source": source,
        #     "version": version
        # }

getfile_app = webapp.WSGIApplication([('/([^/]+)?', GetFileHandler)],debug=False)