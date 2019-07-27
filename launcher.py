#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

import os
import subprocess

_join = os.path.join
root = os.path.dirname(__file__)

python_path = os.pathsep.join([r'C:/Python27/', r'C:/Python27/Scripts', os.path.dirname(root), _join(root, 'scripts')])

os.environ['MAYA_SCRIPT_PATH'] = os.pathsep.join([_join(root, 'mel')])
os.environ['PYTHONPATH'] = r'%s;'.replace('\\', '/') % python_path

subprocess.Popen(r'C:\Program Files\Autodesk\Maya2018\bin\maya.exe', shell=True)

