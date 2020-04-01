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
class PSSM:

    #  the cool PSSM COMMANDs as IDs and STRINGs
    CMD_NULL=0 # NULL or NO COMMAND; is handled as a CMD
    CMD_NULL_STR="NULL"
    CMD_SNA=1 # service not available (SNA); go error state
    CMD_SNA_STR="SNA"
    CMD_PING=2 # send a PING and try get a PONG response
    CMD_PING_STR="PING"
    CMD_PONG=3 # send a PONG for a PING receive
    CMD_PONG_STR="PONG"
    CMD_AKNWLDG=4 # ACKNOWLEDGE a received command
    CMD_AKNWLDG_STR="AKNWLDG"
    CMD_RUN=5 # signal to WAIT to CLIENT or SERVER
    CMD_RUN_STR="RUN"
    CMD_WAIT=6 # signal to WAIT to CLIENT or SERVER
    CMD_WAIT_STR="WAIT"
    CMD_EVENT=7 # signal an EVENT to CLIENT or SERVER
    CMD_EVENT_STR="EVENT"
    CMD_DONE=8 # send a STOP to CLIENT or SERVER
    CMD_DONE_STR="DONE"
    CMD_STOP=9 # send a STOP to CLIENT or SERVER
    CMD_STOP_STR="STOP"
    CMD_STATUS=10 # request the STATUS of CLIENT or SERVER
    CMD_STATUS_STR="STATUS"
    CMD_CONNECT=21 # CONNECT and ready for COMMANDs
    CMD_CONNECT_STR="CONNECT"
    CMD_DISCNCT=22 # DISCONNECT from SERVER
    CMD_DISCNCT_STR="DISCNCT"
    # TODO add your own messages here ..
    CMD_EXAMPLE=42
    CMD_EXAMPLE_STR="EXAMPLE"

    # The cool PSSM STATEs
    STATE_ERROR=0
    STATE_ERROR_STR="ERROR"
    STATE_IDLE=1
    STATE_IDLE_STR="IDLE"
    STATE_RUNNING=2
    STATE_RUNNING_STR="RUNNING"

    # Constructor
    def __init__(self):
        self.data = [] # do some array

    def hello(self):
        return 'Hello World'
