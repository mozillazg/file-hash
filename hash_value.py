#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import zlib
import os
from time import localtime, strftime
import wx

"""输入文件路径返回如下信息：
File path:
Size:
Date modified:
MD5:
SHA1:
CRC32:
"""

# hash 计算 MD5 、SHA1
def hash_value(filename, filesize, maxsize, xhash):
    """提供要计算 hash 值的文件路径、文件大小、每次读取的文件块大小及
    算法的摘要对象
    返回字符串类型的 hash 值
    """
    with open(filename, 'rb') as openfile: # 打开文件，一定要是以二进制打开
        if filesize < maxsize: # 如果是小文件
            data = openfile.read()
            xhash.update(data)
        else: # 大文件
            while True: 
                data = openfile.read(maxsize) # 读取文件块
                if not data: # 直到读完文件
                    break
                xhash.update(data)
    return xhash.hexdigest()


# CRC32 计算 CRC32
def crc32_value(filename, filesize, maxsize):
    """提供要计算 CRC32 值的文件路径、文件大小及每次读取的文件块大小
    返回整型类型的 CRC32 值
    """
    crc = 0
    with open(filename, 'rb') as openfile:
        if filesize < maxsize:
            data = openfile.read()
        else:
            while True:
                data = openfile.read(maxsize)
                if not data:
                    break
                crc = zlib.crc32(data, crc) 
    crc = zlib.crc32(data, crc)
    return '%x' %(crc & 0xffffffff)

def choose_file(event):
    file_p = wx.FileDialog(bkg, 'Choose a file', 
                                        style=wx.DD_DEFAULT_STYLE)
    if file_p.ShowModal() == wx.ID_OK:
        path = file_p.GetPath()
        file_path_txt.SetValue(path)
    file_p.Destroy()
    if file_path_txt.GetValue():
        hash_result()

def hash_result():
    filepath = file_path_txt.GetValue()
    blocksize = 1024 * 1024 # 每次读取的文件块的大小（bytes）
    size = os.path.getsize(filepath) # 文件大小
    date = strftime('%Y/%m/%d %H:%M:%S', # 文件最后修改时间
                                localtime(os.path.getmtime(filepath)))
    md5 = hash_value(filepath, size, blocksize, hashlib.md5()) # 计算 MD5 值
    sha1 = hash_value(filepath, size, blocksize, hashlib.sha1()) # 计算 SHA1 值
    crc32 = crc32_value(filepath, size, blocksize) # CRC32
    
    contents.AppendText('File path: ' + filepath + '\n')
    contents.AppendText('Size: ' + str(size) +' bytes\n')
    contents.AppendText( 'MD5: '+ md5.upper() + '\n')
    contents.AppendText('SHA1: ' + sha1.upper() + '\n')
    contents.AppendText('CRC32: ' + str(crc32).upper() + '\n\n')


if __name__ == '__main__':
    # TO-DO: 拖拽输入文件路径并立即触发求值 Bind()?
    app = wx.App()
    win = wx.Frame(None, title="Python File Hash", size=(500, 335))
    bkg = wx.Panel(win)
    
    chooseButton = wx.Button(bkg, label='Browse...')
    chooseButton.Bind(wx.EVT_BUTTON, choose_file)
    label1 = wx.StaticText(bkg,1,"File path: ")
    file_path_txt = wx.TextCtrl(bkg, -1, "")
    contents = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)
    #file_path_txt.SetDropTarget()
    
    hbox = wx.BoxSizer()
    hbox.Add(label1, proportion=0, flag=wx.ALIGN_CENTRE|wx.ALL, border=5)
    hbox.Add(file_path_txt, 1, wx.EXPAND, 5)
    hbox.Add(chooseButton, 0, wx.LEFT, 5)
    
    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
    vbox.Add(contents, proportion=1,
                        flag=wx.EXPAND | wx.LEFT | wx.BOTTOM 
                        | wx.RIGHT, border=5)
    
    bkg.SetSizer(vbox)
    win.Show()
    
    app.MainLoop()


    ## TO DO: 去除 filepath 首尾的单引号及双引号
    #filepath = raw_input('请输入文件路径：').strip().decode('utf-8')
    #blocksize = 1024 * 1024 # 每次读取的文件块的大小（bytes）
    #size = os.path.getsize(filepath) # 文件大小
    #date = strftime('%Y/%m/%d %H:%M:%S', # 文件最后修改时间
                                #localtime(os.path.getmtime(filepath)))
    #md5 = hash_value(filepath, size, blocksize, hashlib.md5()) # 计算 MD5 值
    #sha1 = hash_value(filepath, size, blocksize, hashlib.sha1()) # 计算 SHA1 值
    #crc32 = crc32_value(filepath, size, blocksize) # CRC32
    
    #print 'File path: %s' % filepath
    #print 'Size: %s bytes' % size
    #print 'Date modified: %s' % date
    ##print 'MD5: %s' % md5
    ##print 'SHA1: %s' % sha1
    ##print 'CRC32: %x' % (crc32 & 0xffffffff)
    ## 处理结果使其中的字母大写
    #print 'MD5: %s' % md5.upper()
    #print 'SHA1: %s' % sha1.upper()
    #print 'CRC32: %X' % (crc32 & 0xffffffff)
