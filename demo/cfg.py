#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys
from os.path import abspath, join, dirname, basename, exists

cur_path = abspath(dirname(__file__))
damo_path = abspath(join(cur_path, '..'))
res_path = join(cur_path, 'res')
pic_path = join(cur_path, 'pic')
tmp_path = join(cur_path, 'tmp')

sys.path.append(damo_path)
from damo import *


def get_res(*args):
    return join(res_path, *args)

def get_pic(*args):
    return join(pic_path, *args)

if not exists(tmp_path):
    os.mkdir(tmp_path)

def get_tmp(*args):
    return join(tmp_path, *args)

def capture(dm, name=None, x1=0, y1=0, x2=None, y2=None):
    if name is None:
        name = join(tmp_path, 'capture.bmp')
    else:
        name = join(tmp_path, name + '.bmp')

    if x2 is None:
        x2 = dm.w
    if y2 is None:
        y2 = dm.h
    return dm.Capture(x1, y1, x2, y2, name)

def rect(x, y, w=20, h=20):
    return dict(x1=x, y1=y, x2=x+w, y2=y+h)

def rect_center(x, y, w=20, h=20):
    w2, h2 = w/2, h/2
    return dict(x1=x-w2, y1=y-h2, x2=x+w2, y2=y+h2)
