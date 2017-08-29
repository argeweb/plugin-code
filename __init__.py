#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
import webapp2
from google.appengine.api.datastore_errors import NeedIndexError
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
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
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


def get_theme_path(theme, path, pre_word=u'themes'):
    templates = u''
    if pre_word != u'themes':
        templates = u"/templates"
    if path.startswith(u'/%s/%s' % (pre_word, theme)) is False:
        path = u'/%s/%s%s/%s' % (pre_word, theme, templates, path)
    if path.startswith('/') is True:
        path = path[1:]
    return path


class GetFileHandler(webapp2.RequestHandler):
    def get_string(self, key='', default_value=u''):
        if key is '':
            return default_value
        try:
            if key not in self.request.params:
                rv = default_value
            else:
                rv = self.request.get(key)
        except:
            rv = default_value
        if rv is None or rv is '' or rv is u'':
            rv = u''
        return rv

    def get(self, request_path):
        from plugins.file.models.file_model import get_file
        from google.appengine.api import namespace_manager
        host_information, namespace, theme, server_name = settings.get_host_information_item()
        namespace_manager.set_namespace(namespace)
        is_min = False
        version = ''

        if request_path.startswith('/assets/') or request_path.startswith('assets/'):
            request_path = request_path.replace('/assets/', '').replace('assets/', '')
            resource = get_file(request_path)
        else:
            request_path = get_theme_path(theme, request_path, self.get_string('dir', u'themes'))
            try:
                resource = get_file(request_path)
                if resource is None:
                    path, version, is_min = get_params_from_file_name(request_path)
                    resource = get_file(path)
                    if resource is None:
                        return self.redirect('/%s' % request_path)
            except NeedIndexError:
                return self.redirect('/%s' % request_path)

        content_type = resource.content_type_or_default
        version = str(resource.last_version) if version is '' else version
        etag = str(request_path) + '||' + version + '||' + str(theme)
        if self.request.headers.get('If-None-Match') == etag:
            return self.abort(304)
        self.response.headers.setdefault('Access-Control-Allow-Origin', '*')
        self.response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
        self.response.headers['Cache-control'] = 'public, max-age=60' if version is '' else 'public, max-age=604800'
        self.response.headers['Content-Type'] = content_type
        self.response.headers['ETag'] = etag
        from models.code_model import CodeModel
        s = CodeModel.get_source(target=resource, version=version)
        if s is None:
            return self.response.out.write('')
        if is_min is True:
            source = s.source_mini
        else:
            source = s.source
        self.response.out.write(source)


getcode = webapp.WSGIApplication([('/(.+)+', GetFileHandler)], debug=False)
