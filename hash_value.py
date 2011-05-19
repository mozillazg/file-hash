#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import zlib
import os
from time import localtime, strftime

# CRC32
def crc32_value(xdata, xcrc=0):
    """提供要计算 CRC32 值的字符串及初始 CRC32 值（可选）
    返回整型类型的 CRC32 值
    """
    crc = zlib.crc32(xdata, xcrc)
    if crc > 0:
        return "%x" % (crc)
    else:
        return "%x" % (~crc ^ 0xffffffff)

if __name__ == '__main__':
    filepath = raw_input('请输入文件路径：').strip().decode('utf-8')
    with open(filepath, 'rb') as openfile:
        data = openfile.read()
    crc32 = 0
    with open(filepath, 'rb') as openfile:
        for data_line in openfile.readlines():
            crc32 = zlib.crc32(data_line, crc32) # CRC32
    md5 = hashlib.md5(data).hexdigest() # 计算 MD5 值
    sha1 = hashlib.sha1(data).hexdigest() # 计算 SHA1 值
    size = os.path.getsize(filepath) # 文件大小
    date = strftime('%Y/%m/%d %H:%M:%S', # 文件最后修改时间
                                localtime(os.path.getmtime(filepath)))
    
    print 'File path: %s' % filepath
    print 'Size: %s bytes' % size
    print 'Date modified: %s' % date
    #print 'MD5: %s' % md5
    #print 'SHA1: %s' % sha1
    #print 'CRC32: %x' % (crc32 & 0xffffffff)
    # 处理结果使其中的字母大写
    print 'MD5: %s' % md5.upper()
    print 'SHA1: %s' % sha1.upper()
    print 'CRC32: %X' % (crc32 & 0xffffffff)
