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
import time, copy, serial, os, pty, threading

class PSSM_CMD:
    TYPE = "CMD"
    def __init__(self, id, str):
        self.ID = id
        self.STR = str

class PSSM_STATE:
    TYPE = "STATE"
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
    def __init__(self, port):
        # The current COMMAND and the NEXT COMMAND
        self.CMD = copy.copy(self.CMD_NULL)
        # The current STATE and the NEXT STATE
        self.STATE = copy.copy(self.STATE_IDLE)
        # open serial ..
        self.ser = serial.Serial( port, 2400, timeout=1 )

    def setup(self):
        # print( "setup .." )
        return ""

    def welcome(self): # some how useless
        # print( "welcome .." )
        return ""

    def ready(self): # some how useless
        # print( "ready .." )
        return ""

    def loop(self):
#        while True:
        self.CMD.ID = self.readCOMMAND( )

        self.STATE = self.process_COMMAND(self.CMD)
        # print( "process_COMMAND" + " - " + "NEXT_STATE:   " + str(self.STATE.ID) + " " + self.STATE.STR )
        self.CMD = self.process_STATE(self.STATE) # next COMMAND is not used here .. is stored by memeber var
        # print( "process_STATE" + "   - " + "next_COMMAND: " + str(self.CMD.ID) + " " + self.CMD.STR )
        # print( " " )
        time.sleep(0.01)

    def process_COMMAND(self, cmd):

        self.CMD = cmd # obvious useless

        next_state = copy.copy(self.STATE) # next state is same state

        # if elif else block goes here
        if cmd.ID == self.CMD_SNA.ID:
            print( self.CMD_SNA.STR )
            next_state = copy.copy(self.STATE_ERROR) # go directly to error state

        elif cmd.ID == self.CMD_PING.ID:
            print( self.CMD_PING.STR )
            if self.STATE.ID == self.STATE_ERROR.ID:  # move out of error state
                next_state = copy.copy(self.STATE_IDLE)
            else: # obvious useless
                next_state = copy.copy(self.STATE)
            writeCOMMAND( self.CMD_PONG.STR )

        elif cmd.ID == self.CMD_PONG.ID:
            print( self.CMD_PONG.STR )
            if self.STATE.ID == self.STATE_ERROR.ID: # move out of error state
                next_state = copy.copy(self.STATE_IDLE)
            else: # obvious useless
                next_state = copy.copy(self.STATE)
            writeCOMMAND( self.CMD_PING.STR )

        elif cmd.ID == self.CMD_AKNWLDG.ID:
            print( self.CMD_AKNWLDG.STR )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMD_RUN.ID:
            print( self.CMD_RUN.STR )
            if self.STATE.ID != self.STATE_ERROR.ID: # move out of error state
                next_state = copy.copy(self.STATE_RUNNING)
                writeCOMMAND( self.ASSM_CMD_AKNWLDG.STR )
            else: # obvious useless
                next_state = copy.copy(self.STATE)

        elif cmd.ID == self.CMD_STOP.ID:
            print( self.CMD_STOP.STR )
            if self.STATE.ID == self.STATE_RUNNING.ID: # move out of error state
                next_state = copy.copy(self.STATE_IDLE)
                writeCOMMAND( self.ASSM_CMD_AKNWLDG.STR )
            else: # obvious useless
                next_state = copy.copy(self.STATE)

        elif cmd.ID == self.CMD_WAIT.ID:
            print( self.CMD_WAIT.STR )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMD_EVENT.ID:
            print( self.CMD_EVENT.STR )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMD_DONE.ID:
            print( self.CMD_DONE.STR )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMD_STATUS.ID:
            print( self.CMD_STATUS.STR )
            writeSTATE( self.STATE.STR )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMD_CONNECT.ID:
            print( self.CMD_CONNECT.STR )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMD_DISCNCT.ID:
            print( self.CMD_DISCNCT.STR )
            next_state = copy.copy(self.STATE) # obvious useless

        else:
            # print( self.CMD_NULL.STR )
            next_state = copy.copy(self.STATE)  # obvious useless

        return next_state

    def process_STATE(self, state):

        self.STATE = state # obvious useless

        next_cmd = copy.copy(self.CMD_NULL) # next command is null

        if state.ID == self.STATE_ERROR.ID:
            # print( self.STATE_ERROR.STR )
            next_cmd = self.error( self.CMD )
        elif state.ID == self.STATE_IDLE.ID:
            # print( self.STATE_IDLE.STR )
            next_cmd = self.idle( self.CMD )
        elif state.ID == self.STATE_RUNNING.ID:
            # print( self.STATE_RUNNING.STR )
            next_cmd = self.running( self.CMD )
        else:
            # print( "DEFAULT STATE" )
            dmy = ""
            # next_cmd is null ..
        return next_cmd


    def readCOMMAND(self):
        cmd = self.CMD_NULL.STR # we read STRINGS; by an example
        ndx = 0
        char = ''
        chars = []
        isReceiving = False
        while self.ser.inWaiting( ):

            char = self.ser.read( ) # read single byte

            if isReceiving == True:
                if cmd != self.MARKER_FOOT :
                    chars[ ndx ] = char
                    ndx = ndx + 1
                    if ndx >= 32:
                        ndx = 31 # stop filling the buffer ..
                        isReceiving = False # stop receiving
                else:
                    isReceiving = False
            elif char == self.MARKER_HEAD :
                isReceiving = True

            def join(s):
                j = ""
                for c in s:
                    j += c
                return j

            cmd = join( chars )

        return cmd


    def writeCOMMAND(self, cmd): # send ID _NOT_ STR to arduino
        final = self.MARKER_HEAD + cmd.ID + self.MARKER_FOOT # e.g. <5>
        print( final ) # send ID _NOT_ STR to arduino
        self.ser.Print( final ) # send ID _NOT_ STR to arduino

    def writeSTATE(self, state):
        final = self.MARKER_HEAD + state.STR + "/" + self.MARKER_FOOT # e.g. <IDLE/>
        print( final )
        self.ser.Print( state.ID )

    def writeData(self, data):
        print( data )
        self.ser.Print( data )

    # overload this method by own needs ..
    def error(self, PSSM_CMD):
        next_cmd = copy.copy(self.CMD_NULL)
        return next_cmd

    # overload this method by own needs ..
    def idle(self, PSSM_CMD):
        next_cmd = copy.copy(self.CMD_NULL)
        return next_cmd

    # overload this method by own needs ..
    def running(self, PSSM_CMD):
        next_cmd = copy.copy(self.CMD_NULL)
        return next_cmd
