#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

plugins_helper = {
    "title": u"線上編輯原始碼",
    "desc": u"可以以動態的方式進行程式碼編輯",
    "controllers": {
        "code_target": {
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
