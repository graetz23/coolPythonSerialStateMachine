#!/usr/bin/python
#
# coolPSSM - cool python serial state machine
#
# Christian
# graetz23@gmail.com
# created 20200401
# version 20200401
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
import serial, os, pty, threading
from threading import Timer, Thread, Event
from coolPSSM import PSSM

# def listener(port):
#     while 1:
#         res = b""
#         while not res.endswith(b"\r\n"):
#             # keep reading one byte at a time until we have a full line
#             res += os.read(port, 1)
#         print("command: %s" % res)
#
#         #write back the response
#         if res == b'QPGS\r\n':
#             os.write(port, b"correct result\r\n")
#         else:
#             os.write(port, b"I dont understand\r\n")

# create some class for threading PSSM ..
class MyThread(Thread):
    def __init__(self, event, coolPSSM):
        Thread.__init__(self)
        self.stopped = event
        self.coolPSSM = coolPSSM

    def run(self):
        while not self.stopped.wait(0.1):
            self.coolPSSM.loop( )

# dummy serial connection for now ..
# master, slave = pty.openpty() #open the pseudoterminal
# master_name = os.ttyname(master) #translate the slave fd to a filename
# print(master_name)
# slave_name = os.ttyname(slave) #translate the slave fd to a filename
# print(slave_name)

# let's do it in arduino style but only in a thread .. ;-)
pssm = PSSM(master_name) # always put some global object

pssm.setup( ) # run setup

while True:
    pssm.loop( ); # looping louie

# #create a separate thread that listens on the master device for commands
# stopFlag = Event()
# thread = MyThread( stopFlag, pssm ) # put it in a thread to loop it
# thread.start()

# while True:
#     input = raw_input('Enter your cool PSSM command:')  # If you use Python 2
#     cmd = '<' + str(input) +  '>'
#     print(cmd)
#     if cmd == "<exit>" or cmd == "<EXIT>":
#         stopFlag.set( )
#     os.write( slave, cmd ) #write the first command
