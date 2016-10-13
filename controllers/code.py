#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/3/3

import datetime
from time import time
from ..models.code_model import CodeModel
from ..models.code_target_model import CodeTargetModel as target_model
from argeweb import settings, Pagination
from argeweb.core.gaeforms import model_form
from argeweb import auth, add_authorizations
from argeweb import Controller, route_with, route, controllers


class Code(Controller):
    class Meta:
        Model = CodeModel

    @route_with('/code/')
    @route_with('/code/<target_name>/edit.html')
    @add_authorizations(auth.require_admin)
    def index(self, target_name=None):
        self.context["body_class"] = "show_list"
        if target_name is None:
            self.context["list"] = target_model.all()
            return

        n = target_model.get_by_name(target_name)
        if n is None:
            n = target_model()
            n.title = target_name
            n.put()
        self.context["body_class"] = "show_record"
        self.context["list"] = [n]


    @route_with('/code/welcome.html')
    @add_authorizations(auth.require_admin)
    def welcome(self):
        pass

    @route_with('/code/records.html')
    @add_authorizations(auth.require_admin)
    def records(self):
        target = self.params.get_ndb_record("target")
        file_type = self.params.get_string("file_type")
        records = self.meta.Model.all_with_target(target, file_type)

        self.context["target"] = target
        self.context["target_key"] = self.params.get_string("target")
        self.context["records"] = records.fetch(50)
        self.context["file_type"] = self.params.get_string("file_type")
        self.context["has_record"] = False
        if records.get() is not None:
            self.context["has_record"] = True

    @route_with('/code/editor.html')
    @add_authorizations(auth.require_admin)
    def editor(self):
        self.context["target"] = self.params.get_string("target")
        self.context["file_type"] = self.params.get_string("file_type")
        self.context["record_key"] = self.params.get_string("record_key")
        self.context["record"] = self.params.get_ndb_record("record_key")

    @route_with('/code/save.json')
    @add_authorizations(auth.require_admin)
    def save_json(self):
        self.meta.change_view("json")
        code = self.params.get_string("code")
        target = self.params.get_ndb_record("target")
        file_type = self.params.get_string("file_type")
        source_minify = u""
        version = int(time()) - 1460000000
        if file_type == "javascript":
            target.js_version = version
            source_minify = self.mini_js(code)
        elif file_type == "css":
            target.css_version = version
            source_minify = self.mini_css(code)
        elif file_type == "html":
            target.html_version = version
        else:
            self.context["data"] = {"error": "Wrong File Type"}
            return
        target.put()

        n = self.meta.Model()
        n.title = u" 版本 " + str(version)
        n.source = code
        n.source_mini = source_minify
        n.version = version
        n.code_type = file_type
        n.target = target.key
        n.put()
        self.context["data"] = {"info": "done"}

    @route_with('/code/<target_name>_info.json')
    def info(self, target_name):
        import os
        self.meta.change_view('jsonp')
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        target = target_model.get_by_name(target_name)
        self.context['data'] = {
            'content': target.title,
            'js-version': target.js_version,
            'css-version': target.css_version,
            'html-version': target.html_version,
            'version': os.environ['CURRENT_VERSION_ID']
        }

    @route_with('/c/<target_name>.html')
    @route_with('/code/<target_name>_<version>.html')
    def html(self, target_name, version=None):
        c = target_model.get_by_name(target_name)
        if version is None:
            version = str(c.html_version)
        s = self.meta.Model.get_source(target=c, code_type="html", version=version)
        source = u""
        if s is not None:
            source = s.source
            version = s.version
        self.context["record"] = {
            "source": source,
            "version": version
        }

    @route_with('/c/<target_name>.js')
    @route_with('/code/<target_name>_<version>.js')
    def js(self, target_name, version=None):
        if self.request.headers.get('If-None-Match'):
            return self.abort(304)
        self.meta.change_view('render')
        c = target_model.get_by_name(target_name)
        if version is None:
            self.response.headers["Cache-control"] = "public, max-age=60"
            version = str(c.js_version)
        else:
            self.response.headers["Cache-control"] = "public, max-age=604800"
        self.response.headers['Content-Type'] = 'text/javascript'
        self.response.headers["ETag"] = target_name + "_" + version
        s = self.meta.Model.get_source(target=c, code_type="javascript", version=version)
        source = u""
        if s is not None:
            source = s.source_mini
        if source is None:
            source = s.source
        self.context["record"] = {
            "target_name": target_name,
            "source": source,
            "version": version
        }

    @route_with('/c/<target_name>.css')
    @route_with('/code/<target_name>_<version>.css')
    def css(self, target_name, version=None):
        if self.request.headers.get('If-None-Match'):
            return self.abort(304)
        c = target_model.get_by_name(target_name)
        if version is None:
            self.response.headers["Cache-control"] = "public, max-age=60"
            version = str(c.css_version)
        else:
            self.response.headers["Cache-control"] = "public, max-age=604800"
        self.response.headers['Content-Type'] = 'text/css'
        self.response.headers["ETag"] = target_name + "_" + version
        self.meta.change_view('render')
        s = self.meta.Model.get_source(target=c, code_type="css", version=version)
        source = u""
        if s is not None:
            source = s.source_mini
        if source is None:
            source = s.source
        self.context["record"] = {
            "target_name": target_name,
            "source": source,
            "version": version
        }

    @route_with('/code/version.json')
    def info(self):
        self.meta.change_view('jsonp')
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        return_dict = {}
        js_file_name = self.params.get_string("js", u"api,channel").split(",")
        for item in js_file_name:
            js = target_model.get_by_name(item)
            return_dict["js-%s-%s" % (item, js.js_version)] = "/code/%s_%s.js" % (item, js.js_version)
        css_file_name = self.params.get_string("css", u"mini").split(",")
        for item in css_file_name:
            css = target_model.get_by_name(item)
            return_dict["css-%s-%s" % (item, css.css_version)] = "/code/%s_%s.css" % (item, css.css_version)
        self.context['data'] = return_dict

    @route_with('/admin/code/plugins_check')
    def admin_plugins_check(self):
        self.meta.change_view('jsonp')
        self.context['data'] = {
            'status': "enable"
        }

    def mini_js(self, js):
        from jsmin import jsmin
        return jsmin(js)

    def mini_css(self, css):
        import sys, re
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
