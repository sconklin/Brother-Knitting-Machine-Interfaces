#!/usr/bin/env python

# Copyright 2010  Steve Conklin 
# steve at conklinhouse dot com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# Note - this was started but has not been tested as I don't have a PDD1 or Brother drive.
# It is likely very broken

# This software dumps disks using the Tandy PDD1

# You will need the (very nice) pySerial module, found here:
# http://pyserial.wiki.sourceforge.net/pySerial

import sys
import os
import os.path
import string
from array import *
import serial

version = '1.0'

class PDDif():

    def __init__(self, basename):
        self.verbose = True
        self.noserial = False
        self.ser = None
        return

    def __del__(self):
        return

    def open(self, cport='/dev/ttyUSB0'):
        if self.noserial is False:
            self.ser = serial.Serial(port=cport, baudrate=9600, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0, dsrdtr=0)
            if self.ser == None:
                print 'Unable to open serial device %s' % cport
                raise IOError
        return

    def close(self, foo):
        if self.noserial is not False:
            if ser:
                ser.close()
        return

    def dumpchars(self):
        num = 1
        while 1:
            inc = self.ser.read()
            if len(inc) != 0:
                print 'flushed 0x%02X (%d)' % (ord(inc), num)
                num = num + 1
            else:
                break
        return

    def readsomechars(self, num):
        sch =  self.ser.read(num)
        return sch

    def readchar(self):
        inc = ''
        while len(inc) == 0:
            inc = self.ser.read()
        return inc
            
    def writebytes(self, bytes):
        self.ser.write(bytes)
        return

    def calcChecksum(self, string):
        sum = 0
        for schr in string:
            sum = sum + ord(schr)
        sum = sum % 0x100
        sum = sum ^ 0xFF
        return chr(sum)

    def getDriveStatus(self):
        ds_string = "ZZ" + chr(7) + chr(0)
        cs = self.calcChecksum(ds_string)
        ds_string = ds_string + cs
        self.writebytes(ds_string)
        self.dumpchars()
        return

    def getDriveCondition(self):
        ds_string = "ZZ" + chr(0x0c) + chr(0)
        cs = self.calcChecksum(ds_string)
        ds_string = ds_string + cs
        self.writebytes(ds_string)
        self.dumpchars()
        return

if len(sys.argv) < 3:
    print '%s version %s' % (sys.argv[0], version)
    print 'Usage: %s basedir serialdevice' % sys.argv[0]
    sys.exit()

print 'Preparing . . . Please Wait'
pdd = PDDif(sys.argv[1])

pdd.open(cport=sys.argv[2])

print 'Ready!'
pdd.getDriveStatus()
pdd.getDriveCondition()

emu.close()
