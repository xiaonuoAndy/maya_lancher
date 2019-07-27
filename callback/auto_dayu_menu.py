#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'


def auto_dayu_menu():

    from fitment import fitment
    fitment()

    import maya
    from py.nodeEditorMenus import _createShaderMenuItems
    maya.app.general.nodeEditorMenus._createShaderMenuItems = _createShaderMenuItems

