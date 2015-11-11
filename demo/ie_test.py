#!/usr/bin/env python
# -*- coding:utf-8 -*-
from damo import *

def ie_test(dm):
    if 0:
        dm = Damo()
    w, h = dm.GetClientSize()
    dm.Capture(0, 0, w, h, r'd:\\tmp\ie.bmp')
    for i in xrange(1):
        x, y = dm.FindPic(0, 0, w, h, u'pic\\ie_new.bmp', sim=0.8)
        if x and y:
            dm.MoveAndClick(x + 30, y + 10)
        sleep(3)

def main():
    dm = Damo()
    dm.SetPath(damo_path)
    if not dm.FindWindow('', 'Internet Ex'):
        print 'fail'
        return
    if not dm.BindWindow(DISPLAY_GDI, MOUSE_NORMAL, KEYPAD_WINDOWS):
        print 'bind fail'
        return
    ie_test(dm)

if __name__ == '__main__':
    main()
