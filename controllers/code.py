#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/3/3
import random
from time import time

from google.appengine.api import channel

from argeweb import auth, add_authorizations
from argeweb import Controller, scaffold
from argeweb import route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search
from ..models.code_target_model import CodeTargetModel
from ..models.code_model import CodeModel
from argeweb.core import json_util


def crete_channel_token(target, timeout=480):
    return channel.create_channel(target, timeout)


def send_message_to_client(client_id, data):
    result = unicode(json_util.stringify(data))
    channel.send_message(client_id, result)


class Code(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 10

    @staticmethod
    def process_path(path):
        content_type = ""
        if path.startswith("/") is False:
            path = "/" + path
        path = path.replace("/assets", "")
        if path.endswith(".css") is True:
            content_type = "css"
        if path.endswith(".html") is True:
            content_type = "html"
        if path.endswith(".js") is True:
            content_type = "javascript"
        return path, content_type

    @route
    def channel(self):
        if self.request.headers.get('If-None-Match'):
            return self.abort(304)
        client_id = None
        if "client_id" in self.session:
            client_id = self.session["client_id"]
        if client_id is None:
            rnd = ''.join([str(random.randint(100, 999)) for x in range(0, 10)])
            client_id = rnd[11:16] + rnd[21:26]
            self.session["client_id"] = client_id
        self.response.headers["ETag"] = self.request.path_url + "_" + client_id
        self.context["remote"] = self.request.path_url
        self.context["token"] = crete_channel_token(client_id)

    @route
    @add_authorizations(auth.require_admin)
    def admin_index(self):
        self.context["target"] = self.params.get_ndb_record("key")

    @route
    @add_authorizations(auth.require_admin)
    def admin_create(self):
        target_name, content_type = self.process_path(self.params.get_string("path"))
        n = CodeTargetModel.find_by_title(target_name)
        info = "error"
        msg = u"檔案已存在"
        html = u""
        if content_type is "":
            msg = u"檔案需為 .js  .css  .html"
        if n is None:
            info = "done"
            msg = u"檔案新增成功!"
            n = CodeTargetModel()
            n.title = target_name
            n.content_type = content_type
            n.put()
            html = u'<div class="col-xs-6 col-sm-4 col-md-3 file-info" data-path="%s" data-content-type="%s"><div class="file"><a href="/admin/code_target/code_editor?key=%s" target="aside_iframe"><div class="file-icon %s"><span>%s</span></div><div class="file-name">%s<br><small>版本：%s</small></div></a></div></div>' \
                   % (n.title, n.content_type, n.key.urlsafe(), n.content_type, n.title.split("/")[-1], n.title, n.last_version)
        self.meta.change_view("json")
        self.context["data"] = {
            "info": info,
            "path": target_name,
            "msg": msg,
            "html": html
        }

    @route
    @add_authorizations(auth.require_admin)
    def admin_records(self):
        target = self.params.get_ndb_record("target")
        content_type = self.params.get_string("content_type")
        records = CodeModel.all_with_target(target, content_type)
        self.meta.change_view("json")
        self.context['data'] = {
            'info': "done",
            'records': records.fetch(15)
        }

    @route
    @add_authorizations(auth.require_admin)
    def editor(self):
        self.context["target"] = self.params.get_string("target")
        self.context["file_type"] = self.params.get_string("file_type")
        self.context["record_key"] = self.params.get_string("record_key")
        self.context["record"] = self.params.get_ndb_record("record_key")

    @route
    @add_authorizations(auth.require_admin)
    def admin_save(self):
        self.meta.change_view("json")
        code = self.params.get_string("code")
        target = self.params.get_ndb_record("target")
        content_type = self.params.get_string("file_type")
        version = int(time()) - 1460000000
        import hashlib
        try:
            m2 = hashlib.md5()
            m2.update(code)
            last_md5 = m2.hexdigest()
        except:
            last_md5 = str(time())
        if last_md5 == target.last_md5:
            self.context["data"] = {"error": "No need to change"}
            return
        target.last_version = version
        target.content_type = content_type
        if content_type == "javascript":
            source_minify = self.mini_js(code)
        elif content_type == "css":
            source_minify = self.mini_css(code)
        elif content_type == "html":
            source_minify = u""
        else:
            self.context["data"] = {"error": "Wrong File Type"}
            return
        target.last_md5 = last_md5
        target.put()

        n = CodeModel()
        n.title = u" 版本 " + str(version)
        n.source = code
        n.source_mini = source_minify
        n.version = version
        n.content_type = content_type
        n.target = target.key
        n.put()
        self.context["data"] = {"info": "done"}
        if "client_id" in self.session:
            send_message_to_client(self.session["client_id"], {
                "action": "code_refresh", "status": "success", "client": self.session["client_id"]
            })

    @route
    @add_authorizations(auth.require_admin)
    def admin_check(self):
        self.meta.change_view("json")
        target_name, content_type = self.process_path(self.params.get_string("path"))
        target = CodeTargetModel.get_or_create(target_name, content_type)
        self.context["data"] = {"send": self.params.get_string("check_md5") == target.last_md5 and "false" or "true"}

    @route
    @add_authorizations(auth.require_admin)
    def admin_upload(self):
        self.meta.change_view("json")
        target_name, content_type = self.process_path(self.params.get_string("path"))
        code = self.params.get_string("code")
        import hashlib
        try:
            m2 = hashlib.md5()
            m2.update(code)
            last_md5 = m2.hexdigest()
        except:
            last_md5 = self.params.get_string("check_md5")
        target = CodeTargetModel.get_or_create(target_name, content_type)
        if last_md5 == target.last_md5:
            self.context["data"] = {"error": "No need to change"}
            return
        version = int(time()) - 1460000000
        target.last_version = version
        target.content_type = content_type
        if content_type == "javascript":
            source_minify = self.mini_js(code)
        elif content_type == "css":
            source_minify = self.mini_css(code)
        elif content_type == "html":
            source_minify = u""
        else:
            self.context["data"] = {"error": "Wrong File Type"}
            return
        target.last_md5 = last_md5
        target.put()
        n = CodeModel()
        n.title = u" 版本 " + str(version)
        n.source = code
        n.source_mini = source_minify
        n.version = version
        n.content_type = content_type
        n.target = target.key
        n.put()
        self.context["data"] = {"info": "done"}

    @route_with('/code/<target_name>_info.json')
    def info(self, target_name):
        import os
        self.meta.change_view('jsonp')
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        target = CodeTargetModel.find_by_title(target_name)
        self.context['data'] = {
            'content': target.title,
            'js-version': target.js_version,
            'css-version': target.css_version,
            'html-version': target.html_version,
            'version': os.environ['CURRENT_VERSION_ID']
        }

    @route_with(template='/<:(assets|code)>/<:(.*)>.html')
    def html(self, c, target_name, version=None):
        target_name, version, is_min = self.get_params(target_name, ".html")
        c = CodeTargetModel.find_by_title(target_name)
        if version is None:
            version = str(c.html_version)
        s = CodeModel.get_source(target=c, content_type="html", version=version)
        if s is None:
            return self.error_and_abort(404)
        self.meta.change_view('render')
        self.context["record"] = {
            "source": s.source,
            "version": s.version
        }

    @route_with('/code/version.json')
    def info(self):
        self.meta.change_view('jsonp')
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        return_dict = {}
        js_file_name = self.params.get_string("js", u"api,channel").split(",")
        for item in js_file_name:
            js = CodeTargetModel.find_by_title(item)
            return_dict["js-%s-%s" % (item, js.js_version)] = "/code/%s_%s.js" % (item, js.js_version)
        css_file_name = self.params.get_string("css", u"mini").split(",")
        for item in css_file_name:
            css = CodeTargetModel.find_by_title(item)
            return_dict["css-%s-%s" % (item, css.css_version)] = "/code/%s_%s.css" % (item, css.css_version)
        self.context['data'] = return_dict

    def get_params(self, target_name, hotfix):
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

    def mini_js(self, js):
        from ..libs.jsmin import jsmin
        return jsmin(js)

    def mini_css(self, css):
        import re
        # remove comments - this will break a lot of hacks :-P
        css = re.sub(r'\s*/\*\s*\*/', "$$HACK1$$", css)  # preserve IE<6 comment hack
        css = re.sub(r'/\*[\s\S]*?\*/', "", css)
        css = css.replace("$$HACK1$$", '/**/')  # preserve IE<6 comment hack

        # url() doesn't need quotes
        css = re.sub(r'url\((["\'])([^)]*)\1\)', r'url(\2)', css)

        # spaces may be safely collapsed as generated content will collapse them anyway
        css = re.sub(r'\s+', ' ', css)

        # shorten collapsable colors: #aabbcc to #abc
        css = re.sub(r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', css)

        # fragment values can loose zeros
        css = re.sub(r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', css)
        return_str = []
        for rule in re.findall(r'([^{]+){([^}]*)}', css):

            # we don't need spaces around operators
            selectors = [re.sub(r'(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])', r'', selector.strip()) for selector in
                         rule[0].split(',')]

            # order is important, but we still want to discard repetitions
            properties = {}
            porder = []
            for prop in re.findall('(.*?):(.*?)(;|$)', rule[1]):
                key = prop[0].strip().lower()
                if key not in porder: porder.append(key)
                properties[key] = prop[1].strip()

            # output rule if it contains any declarations
            if properties:
                return_str.append("%s{%s}" % (
                    ','.join(selectors),
                    ''.join(['%s:%s;' % (key, properties[key]) for key in porder])[:-1]))
        return "".join(return_str)
