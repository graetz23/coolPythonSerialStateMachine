#!/usr/bin/python
#
# coolPSSM - cool python serial state machine
#
# Christian
# graetz23@gmail.com
# created 20200401
# version 20200404
#
# MIT License
#
# Copyright (c) 2020 coolPSSM Christian (graetz23@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import serial, time, os, pty, threading
from threading import Timer, Thread, Event
from coolPSSM import PSSM_Client, PSSM_Command

pssm = PSSM_Client( "/dev/ttyACM0", 9600 ) # always put some global object

while True:
    pssm.writeID( pssm.CMDS.RMD1 ) # always write IDs to ARDUINO
    answer = pssm.getANSWER( )
    print( answer )
    time.sleep( 1 )
    i = 0
    while i < 3 :
        pssm.writeID( PSSM_Command( "70", "A0" ) ) # create fly weight like
        i += 1
        time.sleep( 0.5 )
        answer = pssm.getANSWER( )
        print( answer )
        time.sleep( 0.5 )
    # temp = pssm.getThreadedREAD()
    # print("A0: " + str(temp))
    pssm.writeID( pssm.CMDS.STOP ) # always write IDs to ARDUINO
    answer = pssm.getANSWER( )
    print( answer )
    time.sleep( 1 )
