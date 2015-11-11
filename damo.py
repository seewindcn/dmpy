#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os, sys
import atexit
from os.path import join, abspath, dirname
from time import sleep

from ctypes import *
from comtypes import BSTR
from comtypes.automation import VARIANT
import comtypes.client

VER_2_1142 = '2.1142'
VER_3_1233 = '3.1233'
VER_DEFAULT = VER_3_1233

mouses = [
    'dx.mouse.position.lock.message',
    'dx.mouse.position.lock.api',
    'dx.mouse.focus.input.api',
    'dx.mouse.focus.input.message',
    'dx.mouse.input.lock.api',
    'dx.mouse.clip.lock.api',
    'dx.mouse.state.api',
    'dx.mouse.state.message',
    'dx.mouse.api',
    'dx.mouse.cursor',
]

keybs = [
    'dx.keypad.input.lock.api',
    'dx.keypad.state.api',
    'dx.keypad.api',
]

DISPLAY_NORMAL = 'normal'
DISPLAY_GDI = 'gdi'
DISPLAY_GDI2 = 'gdi2'
DISPLAY_DX = 'dx'
DISPLAY_DX2 = 'dx2'
DISPLAY_DX3 = 'dx3'
MOUSE_NORMAL = 'normal'
MOUSE_WINDOWS = 'windows'
MOUSE_WINDOWS2 = 'windows2'
MOUSE_WINDOWS3 = 'windows3'
MOUSE_DX = 'dx'
MOUSE_DX2 = 'dx2'
KEYPAD_NORMAL = 'normal'
KEYPAD_WINDOWS = 'windows'
KEYPAD_DX = 'dx'

damo_path = dirname(abspath(__file__))

def damo_log(*args):
    print('\t'.join(args))


def PINT(v):
    return POINTER(VARIANT)(VARIANT(v))

def P2V(p):
    return p.contents.value

def reg_dm(dm_dll):
    os.system('regsvr32 %s' % dm_dll)

def unreg_dm(dm_dll):
    os.system('regsvr32 /u %s' % dm_dll)

def create_dm(VER):
    """ 需要注意:dll注册需要管理权限,否则虽然会提示注册成功,但是执行CreateObject失败 """
    if 1:
        global dm_dll
        dm_dll = join(damo_path, 'dm', VER, 'dm.dll')
        sys.path.append(join(damo_path, 'dm', VER, 'gen'))
        import Dm
        Dm.dmsoft._typelib_path_ = dm_dll
    else:
        Dm = comtypes.client.GetModule(dm_dll)

    try:
        dmsoft = comtypes.client.CreateObject(Dm.dmsoft)
        #from comtypes.gen import Dm
        dm = dmsoft.QueryInterface(Dm.Idmsoft)
        return dm
    except:
        # reg_dm(dm_dll)
        # dmsoft = comtypes.client.CreateObject(Dm.dmsoft)
        import traceback
        traceback.print_exc()
        damo_log(u'*******请用管理权限注册dm.dll:%s***************' % dm_dll)
        sys.exit(0)


def ensure_unbindwindow(dm):
    def _exit():
        dm.UnBindWindow()
    return atexit.register(_exit)

class Damo(object):
    def __init__(self, DM_VER=VER_DEFAULT):
        self.hwnd = 0
        self.w, self.h = 0, 0
        self.dm_ver = DM_VER
        self.dm = create_dm(DM_VER)
        self.ver = self.dm.Ver()
        damo_log('dm(%s) loaded!' % self.ver)

    @property
    def isVer2(self):
        return self.dm_ver[0] == 2

    def UnBindWindow(self):
        return self.dm.UnBindWindow()

    def FindWindow(self, class_name='', title_name='', parent=None):
        if not (class_name or title_name):
            return False
        if parent is None:
            self.hwnd = self.dm.FindWindow(class_name, title_name)
        else:
            self.hwnd = self.dm.FindWindowEx(parent, class_name, title_name)

        if self.hwnd != 0:
            damo_log('damo.FindWindow:%s' % self.hwnd)
        return self.hwnd != 0

    def BindWindow(self, display, mouse, keypad, public="", mode=0):
        if not self.hwnd:
            return False

        if public or mode or '.' in mouse or '.' in keypad:
            rs = self.dm.BindWindowEx(self.hwnd,
                display, mouse, keypad, public, mode
                )
        else:
            rs = self.dm.BindWindow(self.hwnd,
                display, mouse, keypad, mode,
                )
        if rs == 1:
            atexit.register(self.UnBindWindow)
            self.w, self.h = self.GetClientSize()
            return True
        return False

    def GetWindowTitle(self):
        return self.dm.GetWindowTitle(self.hwnd)

    def ClientToScreen(self, x, y):
        x1, y1, rs = self.dm.ClientToScreen(self.hwnd, x, y)
        if rs == 1:
            return x1, y1
        return 0, 0

    def SetClipboard(self, str1):
        return self.dm.SetClipboard(str1)

    def GetClipboard(self):
        return self.dm.GetClipboard()

    def SendPaste(self):
        return self.dm.SendPaste(self.hwnd)

    def SetPath(self, path):
        self.dm.SetPath(path) == 1

    def SetMouseDelay(self, type, delay):
        self.dm.SetMouseDelay(type, delay)

    def GetClientRect(self):
        if self.isVer2:
            x1, y1 = PINT(0), PINT(0)
            x2, y2 = PINT(0), PINT(0)
            rs = self.dm.GetClientRect(self.hwnd, x1, y1, x2, y2)
            x1, y1, x2, y2 = P2V(x1), P2V(y1), P2V(x2), P2V(y2)
        else:
            x1, y1, x2, y2, rs = self.dm.GetClientRect(self.hwnd)

        if rs:
            return x1, y1, x2, y2
        return 0, 0, 0, 0

    def GetClientSize(self):
        if self.dm_ver == VER_2_1142:
            w, h = PINT(0), PINT(0)
            rs = self.dm.GetClientSize(self.hwnd, w, h)
            w, h = P2V(w), P2V(h)
        else:
            w, h, rs = self.dm.GetClientSize(self.hwnd)

        if rs:
            return w, h
        return 0, 0

    def SetClientSize(self, w, h):
        self.w = w
        self.h = h
        rs = self.dm.SetClientSize(self.hwnd, w, h)
        return rs == 1

    def Capture(self, x1, y1, x2, y2, file):
        rs = self.dm.Capture(x1, y1, x2, y2, file)
        return rs == 1

    def FindColor(self, x1, y1, x2, y2, color, sim=1.0, dir=0):
        ox, oy = PINT(0), PINT(0)
        rs = self.dm.FindColor(x1, y1, x2, y2, color, sim, dir, ox, oy)
        if rs == 1:
            return P2V(ox), P2V(oy)
        return 0, 0

    def FindPic(self, x1, y1, x2, y2, pic_name, delta_color='000000', sim=1.0, dir=0, mulit=False):
        if not mulit:
            ox, oy = PINT(0), PINT(0)
            rs = self.dm.FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir, ox, oy)
            if rs != -1:
                print "find", pic_name, P2V(ox), P2V(oy)
                return P2V(ox), P2V(oy)
            return 0, 0
        else:
            rs = self.dm.FindPicEx(x1, y1, x2, y2, pic_name, delta_color, sim, dir)
            if rs:
                ss = rs.split('|')
                return map(lambda s: map(int, s.split(',')), ss)
            return None

    def MoveWindow(self, x, y):
        if not self.hwnd:
            return False
        rs = self.dm.MoveWindow(self.hwnd, x, y)
        return rs == 1

    def MoveAndClick(self, x, y):
        self.MoveTo(x, y)
        self.LeftClick()

    def MoveTo(self, x, y):
        rs = self.dm.MoveTo(x, y)
        return rs == 1

    def MoveR(self, rx, ry):
        rs = self.dm.MoveR(rx, ry)
        return rs == 1

    def LeftClick(self):
        rs = self.dm.LeftClick()
        return rs == 1

    def LeftDoubleClick(self):
        rs = self.dm.LeftDoubleClick()
        return rs == 1

    def LeftDown(self):
        rs = self.dm.LeftDown()
        return rs == 1

    def LeftUp(self):
        rs = self.dm.LeftUp()
        return rs == 1

    def RightClick(self):
        rs = self.dm.RightClick()
        return rs == 1

    def RightDown(self):
        rs = self.dm.RightDown()
        return rs == 1

    def RightUp(self):
        rs = self.dm.RightUp()
        return rs == 1

    def LoadPic(self, pic_name):
        rs = self.dm.LoadPic(pic_name)
        return rs == 1

    def SetDict(self, index, file):
        rs = self.dm.SetDict(index, file)
        if rs:
            self.UseDict(index)
        return rs == 1

    def UseDict(self, index):
        rs = self.dm.UseDict(index)
        return rs == 1

    def SaveDict(self, index,file):
        rs = self.dm.SaveDict(index,file)
        return rs == 1

    def AddDict(self, index,dict_info):
        rs = self.dm.AddDict(index,dict_info)
        return rs == 1

    def FindStr(self, x1, y1, x2, y2, string, color_format, sim):
        intX, intY = PINT(0), PINT(0)
        rs = self.dm.FindStr(x1, y1, x2, y2, string, color_format, sim, intX, intY)
        return rs

    def FindStrEx(self, x1,y1,x2,y2,string,color_format,sim):
        return self.dm.FindStrEx(x1,y1,x2,y2,string,color_format,sim)

    def FindStrFast(self, x1,y1,x2,y2,string,color_format,sim):
        intX, intY = PINT(0), PINT(0)
        rs = self.dm.FindStrFast(x1,y1,x2,y2,string,color_format,sim, intX, intY)
        return rs

    def FindStrFastEx(self, x1, y1, x2, y2, string, color_format, sim):
        if isinstance(string, unicode):
            string = string.encode('gbk')
        return self.dm.FindStrFastEx(x1,y1,x2,y2,string,color_format,sim)

    def FindString(self, hwnd, addr_range, string_value,type):
        return self.dm.FindString(hwnd, addr_range, string_value,type)

    def Ocr(self, x1,y1,x2,y2,color_format,sim):
        return self.dm.Ocr(x1,y1,x2,y2,color_format,sim)

    def OcrEx(self, x1,y1,x2,y2,color_format,sim):
        return self.dm.OcrEx(x1,y1,x2,y2,color_format,sim)

    def OcrInFile(self, x1, y1, x2, y2, pic_name, color_format, sim):
        return self.dm.OcrInFile(x1, y1, x2, y2, pic_name, color_format, sim)

    def Play(self, media_file):
        """ mp3,wav """
        rs = self.dm.Play(media_file)
        return rs == 1

    def Beep(self, f,duration):
        rs = self.dm.Beep(f,duration)
        return rs == 1








