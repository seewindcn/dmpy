#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cfg import *

def test1(dm):
    """
    :type dm: Damo
    """
    print dm.GetWindowTitle()
    print dm.GetClientSize()
    print dm.ClientToScreen(1,1)


def eve_jump(dm):
    """
    :type dm: Damo
    """
    test1(dm); return

    w, h = dm.w, dm.h
    # w, h = 1024, 768
    # dm.SetClientSize(w, h)

    sleep(1)
    dm.SetDict(0, get_res('eve.txt'))
    capture(dm)
    capture(dm, name='capture1', **rect_center(822, 110))

    if 1:
        dm.MoveAndClick(822, 110)
        sleep(0.2)
        dm.LeftDoubleClick()

    if 0:
        rs = dm.FindStrFastEx(0, 0, w, h, u'跃迁', 'd5d1cd-303030', 0.8); print rs
        rs = dm.OcrEx(0, 0, w, h, 'd5d1cd-202020|d5d1cd-303030|d5d1cd-404040', 0.8); print rs
        dm.SetDict(1, get_res('eve-icon.txt'))
        rs = dm.OcrEx(w-270,0,w,200, '8b8684-303030', 0.7); print rs

    print 'done'
##    while 1:
##        x, y = dm.FindPic(0, 0, w, h, u'pic\\icon跳跃.bmp', sim=0.8)
##        if not (x and y):
##            x, y = dm.FindPic(0, 0, w, h, u'pic\\icon进站.bmp', sim=0.8)
##        if x and y:
##            dm.MoveAndClick(x, y)
##        sleep(3)
##        while 1:
##            x, y = dm.FindPic(0, 0, w, h, u'pic\\跃迁引擎启动.bmp', sim=0.8)
##            if not(x and y):
##                break
##            sleep(2)

def main():
    dm = Damo(VER_3_1233)
    dm.SetPath(tmp_path)
    if not dm.FindWindow('', 'EVE'):
        print 'fail'
        return
    # if not dm.BindWindow(DISPLAY_GDI, MOUSE_NORMAL, KEYPAD_NORMAL):
    if not dm.BindWindow(DISPLAY_GDI2, MOUSE_WINDOWS, KEYPAD_WINDOWS, mode=0):
        print 'bind fail'
        return
    try:
        eve_jump(dm)
    finally:
        dm.UnBindWindow()


if __name__ == '__main__':
    main()
