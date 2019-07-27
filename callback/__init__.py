#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'


import pymel.core as pm
from auto_dayu_menu import auto_dayu_menu

pm.scriptJob(event=('SceneOpened', auto_dayu_menu))
