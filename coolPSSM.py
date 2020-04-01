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
import time, copy

class PSSM_CMD:
    def __init__(self, id, str):
        self.ID = id
        self.STR = str

class PSSM_STATE:
    def __init__(self, id, str):
        self.ID = id
        self.STR = str

class PSSM:

    #  the cool PSSM COMMANDs as IDs and STRINGs
    CMD_NULL    = PSSM_CMD( 0, "NULL" ) # NULL or NO COMMAND; is handled as a CMD
    CMD_SNA     = PSSM_CMD( 1," SNA" ) # service not available (SNA); go error state
    CMD_PING    = PSSM_CMD( 2," PING" ) # send a PING and try get a PONG response
    CMD_PONG    = PSSM_CMD( 3," PONG" ) # send a PONG for a PING receive
    CMD_AKNWLDG = PSSM_CMD( 4," AKNWLDG" ) # ACKNOWLEDGE a received command
    CMD_RUN     = PSSM_CMD( 5," RUN" ) # signal to WAIT to CLIENT or SERVER
    CMD_WAIT    = PSSM_CMD( 6," WAIT" ) # signal to WAIT to CLIENT or SERVER
    CMD_EVENT   = PSSM_CMD( 7," EVENT" ) # signal an EVENT to CLIENT or SERVER
    CMD_DONE    = PSSM_CMD( 8," DONE" ) # send a STOP to CLIENT or SERVER
    CMD_STOP    = PSSM_CMD( 9," STOP" ) # send a STOP to CLIENT or SERVER
    CMD_STATUS  = PSSM_CMD( 10, "STATUS" ) # request the STATUS of CLIENT or SERVER
    CMD_CONNECT = PSSM_CMD( 21, "CONNECT" ) # CONNECT and ready for COMMANDs
    CMD_DISCNCT = PSSM_CMD( 22, "DISCNCT" ) # DISCONNECT from SERVER
    # TODO add your own messages here ..
    CMD_EXAMPLE = PSSM_CMD( 42, "EXAMPLE" )

    # The cool PSSM STATEs
    STATE_ERROR     = PSSM_STATE( 0, "ERROR " )
    STATE_IDLE      = PSSM_STATE( 1, "IDLE" )
    STATE_RUNNING   = PSSM_STATE( 2, "RUNNING" )

    MARKER_HEAD = '<' # starting marker for a command on serial line
    MARKER_FOOT = '>' # ending marker for a command on serial line
    MARKER_CMD = 'CMD_' # prefix for commands

    # Constructor
    def __init__(self):
        # The current COMMAND and the NEXT COMMAND
        self.CMD = copy.copy(self.CMD_NULL)
        self.NEXT_CMD = copy.copy(self.CMD) # not necessary; for testing
        # The current STATE and the NEXT STATE
        self.STATE = copy.copy(self.STATE_IDLE)
        self.NEXT_STATE = copy.copy(self.STATE) # not necessary; for testing

    def setup(self):
        print( "setup .." )

    def welcome(self): # some how useless
        print( "welcome .." )

    def ready(self): # some how useless
        print( "ready .." )

    def loop(self):
        print( "loop .." )
        while True:
            next_cmd = self.process_COMMAND(self.CMD)
            next_state = self.process_STATE(self.STATE)
            time.sleep(1)

    def process_COMMAND(self, cmd):
        next_cmd = copy.copy(self.CMD_NULL) # next is no command
        print( "process_COMMAND" + " - " + "next_COMMAND: " + str(next_cmd.ID) + " " + next_cmd.STR )
        return next_cmd

    def process_STATE(self, state):
        next_state = copy.copy(self.STATE) # next is this state
        print( "process_STATE" + "   - " + "next_STATE:   " + str(next_state.ID) + " " + next_state.STR )
        return next_state
