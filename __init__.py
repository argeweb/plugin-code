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
    'title': u'線上編輯原始碼',
    'desc': u'可以以動態的方式進行程式碼編輯',
    'controllers': {
        'code': {
            'group': u'原始碼',
            'actions': [
                {'action': 'list', 'name': u'線上編輯器'},
                {'action': 'add', 'name': u'新增原始碼'},
                {'action': 'edit', 'name': u'編輯原始碼'},
                {'action': 'view', 'name': u'檢視原始碼'},
                {'action': 'delete', 'name': u'刪除原始碼'},
            ]
        }
    }
}


def get_params_from_file_name(path):
    is_min = False
    check_min = path.split('.min')
    if len(check_min) >= 2:
        is_min = True
        path = check_min[0] + check_min[1]
    try:
        version = path.split('/')[-1].split('_')[-1].split('.')[0]
        version = int(version)
        path = path.split('_'+str(version))[0]
    except:
        version = ''
    return path, str(version), is_min

def get_theme_path(theme, path):
    if path.startswith(u'/themes/%s' % theme) is False:
        path = u'/themes/%s/%s' % (theme, path)
    if path.startswith('/') is True:
        path = path[1:]
    return path


class GetFileHandler(webapp2.RequestHandler):
    def get(self, request_path):
        from plugins.file.models.file_model import get_file
        from google.appengine.api import namespace_manager
        host_information, namespace, theme = settings.get_host_information_item()
        namespace_manager.set_namespace(namespace)
        if request_path.startswith('assets/') is True:
            request_path = request_path[7:]
        else:
            request_path = get_theme_path(theme, request_path)
        version = ''
        is_min = False
        c = get_file(request_path)
        if c is None:
            path, version, is_min = get_params_from_file_name(request_path)
            c = get_file(path)
            if c is None:
                import os.path
                if os.path.exists(request_path):
                    return self.redirect('/r/%s' % request_path)
                if os.path.exists(path):
                    return self.redirect('/r/%s' % path)
                return self.abort(404)
        content_type = c.content_type_or_default
        version = str(c.last_version) if version is '' else version
        etag = str(request_path) + '||' + version + '||' + str(theme)
        if self.request.headers.get('If-None-Match') == etag:
            return self.abort(304)
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        self.response.headers['Cache-control'] = 'public, max-age=60' if version is '' else 'public, max-age=604800'
        self.response.headers['Content-Type'] = content_type
        self.response.headers['ETag'] = etag
        from models.code_model import CodeModel
        s = CodeModel.get_source(target=c, version=version)
        if s is None:
            return self.response.out.write('')
        if is_min is True:
            source = s.source_mini
        else:
            source = s.source
        self.response.out.write(source)

getcode = webapp.WSGIApplication([('/(.+)+', GetFileHandler)],debug=False)