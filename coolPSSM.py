#
# coolPSSM - cool python serial state machine
#
# TODO write some description
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
import time, copy, serial, os, pty, threading
from threading import Timer, Thread, Event

# run the reading loop in a thread for receiving from ARDUINO
class PSSM_Serial_Thread (threading.Thread):

    READ = None

    def __init__(self, event, pssm):

        threading.Thread.__init__(self)
        self.stopped = event # obvious useless
        self.runnig = True # obvious useless

        self.PSSM = pssm

    def shutdown(self):
        self.runnig = False
        pass

    def stop(self):
        self.runnig = False

    def run(self):
        while not self.stopped.wait(0.01) and self.runnig:
            try:
                self.READ = self.PSSM.SERIAL.reading( ) # read serial data only
            except:
                pass
            time.sleep(0.01)

# representing a COMMAND by ID (for arduino) and STR (for python)
class PSSM_COMMAND:

    ID = None # for iterating members; do NOT CHANGE the order
    TAG = None # for iterating members; do NOT CHANGE the order

    def __init__(self, id, tag):
        self.ID = id
        self.TAG = tag

    # COPY CONSTRUCTOR in python ~8>
    def COPY(self):
        return copy.copy(self)

    # this is the STYLE to send from PYTHON to ARDUINO
    def genNUM(self):
        return "<" + str(self.ID) + ">"

    # this is the STYLE to send from ARDUINO & PYTHON to PYTHON
    def genTAG(self):
        return "<" + str(self.TAG) + "/>"

# representing a STATE by ID (for arduino) and STR (for python)
class PSSM_STATE:

    ID = None # for iterating members; do NOT CHANGE the order
    TAG = None # for iterating members; do NOT CHANGE the order

    def __init__(self, id, tag):
        self.ID = id
        self.TAG = tag

    # COPY CONSTRUCTOR in python ~8>
    def COPY(self):
        return copy.copy(self)

    # this is the STYLE to send from PYTHON to ARDUINO
    def genNUM(self):
        return "<" + str(self.ID) + ">"

    # this is the STYLE to send from ARDUINO & PYTHON to PYTHON
    def genTAG(self):
        return "<" + str(self.TAG) + "/>"

# This is to send data; however here is NO numerical ID while it is not forseen
# to send data from PYTHON to ARDUINO
class PSSM_DATA:

    TAG = None # for iterating members; do NOT CHANGE the order
    DATA = None # for iterating members; do NOT CHANGE the order

    def __init__(self, tag, data):
        self.TAG = tag
        self.DATA = data

    # COPY CONSTRUCTOR in python ~8>
    def COPY(self):
        return copy.copy(self)

    # this is the STYLE to send ARDUINO & PYTHON to PYTHON
    def genTAG(self):
        return "<" + self.TAG + ">" + str(self.DATA) + "</" + self.TAG + ">"

# representing an itertable set of all COMMANDs that ARDUINO / PYTHON can use to
# intercommunication. ARDUINO receives IDs, while PYTHON receives STRINGS. The
# IDs are SYNC to the ITERATOR stuff of python; keep this!
class PSSM_COMMANDS:

    NULL = None # for iterating members; do NOT CHANGE the order
    SNA  = None # for iterating members; do NOT CHANGE the order
    PING = None # for iterating members; do NOT CHANGE the order
    PONG = None # for iterating members; do NOT CHANGE the order
    AKNW = None # for iterating members; do NOT CHANGE the order
    RUN  = None # for iterating members; do NOT CHANGE the order
    WAIT = None # for iterating members; do NOT CHANGE the order
    EVNT = None # for iterating members; do NOT CHANGE the order
    DONE = None # for iterating members; do NOT CHANGE the order
    STOP = None # for iterating members; do NOT CHANGE the order
    STAT = None # for iterating members; do NOT CHANGE the order
    RMD1 = None # for iterating members; do NOT CHANGE the order
    RMD2 = None # for iterating members; do NOT CHANGE the order
    RMD3 = None # for iterating members; do NOT CHANGE the order
    RMD4 = None # for iterating members; do NOT CHANGE the order
    RMD5 = None # for iterating members; do NOT CHANGE the order
    RMD6 = None # for iterating members; do NOT CHANGE the order
    RMD7 = None # for iterating members; do NOT CHANGE the order
    CNCT = None # for iterating members; do NOT CHANGE the order
    DCNT = None # for iterating members; do NOT CHANGE the order

    def __init__(self):
        #  the cool PSSM & ASSM COMMANDs as IDs and STRINGs
        self.NULL = PSSM_COMMAND(  0, "NULL" ) # NULL or NO COMMAND; is handled as a CMD
        self.SNA  = PSSM_COMMAND(  1," SNA" ) # service not available (SNA); go error state
        self.PING = PSSM_COMMAND(  2," PING" ) # send a PING and try get a PONG response
        self.PONG = PSSM_COMMAND(  3," PONG" ) # send a PONG for a PING receive
        self.AKNW = PSSM_COMMAND(  4," AKNW" ) # ACKNOWLEDGE a received command
        self.RUN  = PSSM_COMMAND(  5," RUN" ) # signal to WAIT to CLIENT or SERVER
        self.WAIT = PSSM_COMMAND(  6," WAIT" ) # signal to WAIT to CLIENT or SERVER
        self.EVNT = PSSM_COMMAND(  7," EVNT" ) # signal an EVENT to CLIENT or SERVER
        self.DONE = PSSM_COMMAND(  8," DONE" ) # send a STOP to CLIENT or SERVER
        self.STOP = PSSM_COMMAND(  9," STOP" ) # send a STOP to CLIENT or SERVER
        self.STAT = PSSM_COMMAND( 10, "STAT" ) # request the STATUS of CLIENT or SERVER
        self.RMD1 = PSSM_COMMAND( 11, "RMD1" ) # let arduino do something while in run MODE 1
        self.RMD2 = PSSM_COMMAND( 12, "RMD2" ) # let arduino do something while in run MODE 2
        self.RMD3 = PSSM_COMMAND( 13, "RMD3" ) # let arduino do something while in run MODE 3
        self.RMD4 = PSSM_COMMAND( 14, "RMD4" ) # let arduino do something while in run MODE 4
        self.RMD5 = PSSM_COMMAND( 15, "RMD5" ) # let arduino do something while in run MODE 5
        self.RMD6 = PSSM_COMMAND( 16, "RMD6" ) # let arduino do something while in run MODE 6
        self.RMD7 = PSSM_COMMAND( 17, "RMD7" ) # let arduino do something while in run MODE 7
        self.CNCT = PSSM_COMMAND( 18, "CNCT" ) # obvious useless yet
        self.DCNT = PSSM_COMMAND( 19, "DCNT" ) # obvious useless yet

# The STATES that ARDUINO / PYTHON can state while running. PYTHON sends IDs to
# ARDUINO, while ARDUINO sends STRINGS to PYTHON; however STATEs are only SENT
# as STRINGS in case of an ID based STAT (status) COMMAND request.
class PSSM_STATES:

    ERROR = None # for iterating members; do NOT CHANGE the order
    IDLNG = None # for iterating members; do NOT CHANGE the order
    MODE1 = None # for iterating members; do NOT CHANGE the order
    MODE2 = None # for iterating members; do NOT CHANGE the order
    MODE3 = None # for iterating members; do NOT CHANGE the order
    MODE4 = None # for iterating members; do NOT CHANGE the order
    MODE5 = None # for iterating members; do NOT CHANGE the order
    MODE6 = None # for iterating members; do NOT CHANGE the order
    MODE7 = None # for iterating members; do NOT CHANGE the order

    def __init__(self):

        #  the cool PSSM & ASSM STATEs as IDs and STRINGs
        self.ERROR = PSSM_STATE( 0, "ERROR " ) # arduino is in ERROR state
        self.IDLNG = PSSM_STATE( 1, "IDLNG" ) # arduino is IDILING around
        # run MODEs; MODE1, MODE2, .., MODE7
        self.MODE1 = PSSM_STATE( 11, "MODE1" ) # arduino is processing MODE 1
        self.MODE2 = PSSM_STATE( 12, "MODE2" ) # arduino is processing MODE 2
        self.MODE3 = PSSM_STATE( 13, "MODE3" ) # arduino is processing MODE 3
        self.MODE4 = PSSM_STATE( 14, "MODE4" ) # arduino is processing MODE 4
        self.MODE5 = PSSM_STATE( 15, "MODE5" ) # arduino is processing MODE 5
        self.MODE6 = PSSM_STATE( 16, "MODE6" ) # arduino is processing MODE 6
        self.MODE7 = PSSM_STATE( 17, "MODE7" ) # arduino is processing MODE 7

# Utilizes the serial console, especially the reading method for receiving
# IDs and / or STRINGs. However, the reading methods should be always threaded.
class PSSM_Serial:

    SER = None # serial console set to NULL

    # Constructor
    def __init__(self, port, baud):

        self.SER = serial.Serial( port, baud, timeout=1 )
        time.sleep(0.1) # give some MOMENT in time to ARDUINO

    def getSerial(self):
        return self.SER

    def isOpen(self):
        return self.SER.isOpen()

    def getPort(self):
        port = None
        if self.isOpen():
            port = self.SER.port
        return port

    def getBaud(self):
        baud = None
        if self.isOpen():
            baud = self.SER.baudrate
        return baud

    def reading(self):
        message = "" # we read STRINGS; by an example
        chars = b"" # read BYTES first
        if self.isOpen(): # obvious useless ??
            while self.SER.inWaiting( ):
                chars += self.SER.read_until( '>' ) # read single byte
        message = str( chars ) # transform BYTES to STRING
        return message

    # Send COMMAND as ID from PYTHON to ARDUINO
    def writeNUM(self, CMD_or_STATE):
        isWritten = False
        if self.isOpen( ) :
            print( CMD_or_STATE.genNUM( ) ) # DEBUG print out; delete later
            self.SER.write( CMD_or_STATE.genNUM( ) ) # send ID to ARDUINO
            isWritten = True
        return isWritten

    # Send COMMAND as TAG to PYHON
    def writeTAG(self, CMD_or_STATE_or_DATA): # send ID _NOT_ STR to arduino
        isWritten = False
        if self.isOpen( ) :
            print( CMD_or_STATE_or_DATA.genTAG( ) ) # DEBUG print out; delete later
            self.SER.write( CMD_or_STATE_or_DATA.genTAG( ) ) # send ID _NOT_ STR to arduino
            isWritten = True
        return isWritten

# TOOL for exploding read COMMANDs baking PSSM_STATE & PSSM_COMMAND objects ..
class PSSM_XML:

    CMDS = None # obvious useless in python

    STATES = None # obvious useless in python

    def __init__(self):

        self.CMDS   = PSSM_COMMANDS() # PROTOTYPEs that can be iterated

        self.STATES = PSSM_STATES() # PROTOTYPEs that can be iterated

    def bake(self, read):
        # TODO analysie the READ by string explosion BAKE then the matching ..
        obj = self.CMDS.NULL.COPY( )
        return obj

    # TODO rewrite it in python's super best style
    # e.g. <DATA>23.72</DATA> => 23.72 - works! but being super nasty!
    def explodeData(self, data):
        tmp0 = data.split('>')
        tmp1 = tmp0[ 1 ].split('<')
        extract  = tmp1[ 0 ]
        return extract

class PSSM_Client():

    CMDS = None # obvious useless in python

    STATES = None # obvious useless in python

    SERIAL = None # obvious useless in python

    THREAD_READING = None # obvious useless in python

    # Constructor
    def __init__(self, port, baud):

        self.CMDS   = PSSM_COMMANDS() # PROTOTYPEs that can be iterated

        self.STATES = PSSM_STATES() # PROTOTYPEs that can be iterated

        self.SERIAL = PSSM_Serial(port, baud) # GETTIN high on SERIAL

        self.threadStopFlag = Event()
        self.THREAD_READING = PSSM_Serial_Thread(self.threadStopFlag, self)
        self.THREAD_READING.start()

class PSSM_Server:

    CMDS = None # obvious useless in python

    STATES = None # obvious useless in python

    SERIAL = None # obvious useless in python

    THREAD_READING = None # obvious useless in python

    CMD = None

    STATE = None

    MARKER_HEAD = '<' # starting marker for a command on serial line
    MARKER_FOOT = '>' # ending marker for a command on serial line

    # Constructor
    def __init__(self, port, baud):

        self.CMDS   = PSSM_COMMANDS() # PROTOTYPEs that can be iterated

        self.STATES = PSSM_STATES() # PROTOTYPEs that can be iterated

        self.SERIAL = PSSM_Serial(port, baud) # GETTIN high on SERIAL

        self.CMD = self.CMDS.NULL.COPY( )

        self.STATE = self.STATES.IDLE.COPY( )

        self.threadStopFlag = Event()
        self.THREAD_READING = PSSM_Serial_Thread(self.threadStopFlag, self)
        self.THREAD_READING.start()

    # Let's keep ARDUINO STYLE in python
    def setup(self):
        # print( "setup .." )
        return ""

    # Let's keep ARDUINO STYLE in python
    def loop(self):

        #while True:
        read = self.THREAD_READING.READ # TODO THIS is not SYNC YET

        if len(read) > 0  :
            # TODO convert the the STRING COMMAND to match an OBJECT
            print( read )

        self.CMD = self.CMDS.IDLE.COPY( )

        self.STATE = self.process_COMMAND(self.CMD)
        print( "process_COMMAND" + " - " + "NEXT_STATE:   " + str(self.STATE.ID) + " " + self.STATE.TAG ) # DEBUG print out; delete later

        self.CMD = self.process_STATE(self.STATE) # next COMMAND is not used here .. is stored by memeber var
        print( "process_STATE" + "   - " + "next_COMMAND: " + str(self.CMD.ID) + " " + self.CMD.TAG ) # DEBUG print out; delete later

        print( " " ) # DEBUG print out; delete later
        time.sleep(1) # DEBUG print out; delete later

    # TODO MATCH the METHODS BELOW TO NEW OBJECT-ORIENTED STYLE ..

    def process_COMMAND(self, cmd):

        self.CMD = cmd # obvious useless

        next_state = copy.copy(self.STATE) # next state is same state

        # if elif else block goes here
        if cmd.ID == self.CMDS.SNA.ID:
            print( self.CMDS.SNA.TAG ) # DEBUG print out; delete later
            next_state = copy.copy(self.STATE_ERROR) # go directly to error state

        elif cmd.ID == self.CMDS.PING.ID:
            print( self.CMDS.PING.TAG )
            if self.STATE.ID == self.STATE_ERROR.ID:  # move out of error state
                next_state = copy.copy(self.STATE_IDLE)
            else: # obvious useless
                next_state = copy.copy(self.STATE)
            writeCommandAsString( self.CMDS.PONG )

        elif cmd.ID == self.CMDS.PONG.ID:
            print( self.CMDS.PONG.TAG )
            if self.STATE.ID == self.STATE_ERROR.ID: # move out of error state
                next_state = copy.copy(self.STATE_IDLE)
            else: # obvious useless
                next_state = copy.copy(self.STATE)
            writeCommandAsString( self.CMDS.PING )

        elif cmd.ID == self.CMDS.AKNW.ID:
            print( self.CMDS.AKNW.TAG )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.RUN.ID:
            print( self.CMDS.RUN.TAG )
            if self.STATE.ID == self.STATE_MODE1.ID: # just ACKNOWLEDGE
                next_state = copy.copy(self.STATE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE2.ID: # just ACKNOWLEDGE
                next_state = copy.copy(self.STATE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE3.ID: # just ACKNOWLEDGE
                next_state = copy.copy(self.STATE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE4.ID: # just ACKNOWLEDGE
                next_state = copy.copy(self.STATE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE5.ID: # just ACKNOWLEDGE
                next_state = copy.copy(self.STATE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE6.ID: # just ACKNOWLEDGE
                next_state = copy.copy(self.STATE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE7.ID: # just ACKNOWLEDGE
                next_state = copy.copy(self.STATE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            else: # obvious useless
                next_state = copy.copy(self.STATE)

        elif cmd.ID == self.CMDS.STOP.ID:
            print( self.CMDS.STOP.TAG )
            if self.STATE.ID == self.STATE_MODE1.ID: # move to IDLE
                next_state = copy.copy(self.STATE_IDLE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE2.ID: # move to IDLE
                next_state = copy.copy(self.STATE_IDLE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE3.ID: # move to IDLE
                next_state = copy.copy(self.STATE_IDLE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE4.ID: # move to IDLE
                next_state = copy.copy(self.STATE_IDLE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE5.ID: # move to IDLE
                next_state = copy.copy(self.STATE_IDLE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE6.ID: # move to IDLE
                next_state = copy.copy(self.STATE_IDLE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            elif self.STATE.ID == self.STATE_MODE7.ID: # move to IDLE
                next_state = copy.copy(self.STATE_IDLE)
                writeCommandAsString( self.ASSM_CMDS.AKNW )
            else: # obvious useless
                next_state = copy.copy(self.STATE)

        elif cmd.ID == self.CMDS.WAIT.ID:
            print( self.CMDS.WAIT.TAG )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.EVENT.ID:
            print( self.CMDS.EVENT.TAG )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.DONE.ID:
            print( self.CMDS.DONE.TAG )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.STATUS.ID:
            print( self.CMDS.STATUS.TAG )
            next_state = copy.copy(self.STATE) # obvious useless
            writeStateAsStr( self.STATE )

        elif cmd.ID == self.CMDS.CONNECT.ID:
            print( self.CMDS.CONNECT.TAG )
            next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.DISCNCT.ID:
            print( self.CMDS.DISCNCT.TAG )
            next_state = copy.copy(self.STATE) # obvious useless

        # RUN MODEs ..

        elif cmd.ID == self.CMDS.RNMD1.ID:
            print( self.ASSM_CMDS.RNMD1.TAG )
            if self.STATE.ID != self.STATE_ERROR.ID:
                print( self.STATE_MODE1.TAG )
                next_state = copy.copy( self.STATE_MODE1 )
            else:
                next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.RNMD2.ID:
            print( self.ASSM_CMDS.RNMD2.TAG )
            if self.STATE.ID != self.STATE_ERROR.ID:
                print( self.STATE_MODE2.TAG )
                next_state = copy.copy( self.STATE_MODE2 )
            else:
                next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.RNMD3.ID:
            print( self.ASSM_CMDS.RNMD3.TAG )
            if self.STATE.ID != self.STATE_ERROR.ID:
                print( self.STATE_MODE3.TAG )
                next_state = copy.copy( self.STATE_MODE3 )
            else:
                next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.RNMD4.ID:
            print( self.ASSM_CMDS.RNMD4.TAG )
            if self.STATE.ID != self.STATE_ERROR.ID:
                print( self.STATE_MODE4.TAG )
                next_state = copy.copy( self.STATE_MODE4 )
            else:
                next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.RNMD5.ID:
            print( self.ASSM_CMDS.RNMD5.TAG )
            if self.STATE.ID != self.STATE_ERROR.ID:
                print( self.STATE_MODE5.TAG )
                next_state = copy.copy( self.STATE_MODE5 )
            else:
                next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.RNMD6.ID:
            print( self.ASSM_CMDS.RNMD6.TAG )
            if self.STATE.ID != self.STATE_ERROR.ID:
                print( self.STATE_MODE6.TAG )
                next_state = copy.copy( self.STATE_MODE6 )
            else:
                next_state = copy.copy(self.STATE) # obvious useless

        elif cmd.ID == self.CMDS.RNMD7.ID:
            print( self.ASSM_CMDS.RNMD7.TAG )
            if self.STATE.ID != self.STATE_ERROR.ID:
                print( self.STATE_MODE7.TAG )
                next_state = copy.copy( self.STATE_MODE7 )
            else:
                next_state = copy.copy(self.STATE) # obvious useless

        else:
            # print( self.CMDS.NULL.TAG )
            next_state = copy.copy(self.STATE)  # obvious useless

        return next_state

    def process_STATE(self, state):

        self.STATE = state # obvious useless

        next_cmd = copy.copy(self.CMDS.NULL) # next command is null

        if state.ID == self.STATE_ERROR.ID:
            # print( self.STATE_ERROR.TAG )
            next_cmd = self.error( self.CMD )

        elif state.ID == self.STATE_IDLE.ID:
            # print( self.STATE_IDLE.TAG )
            next_cmd = self.idle( self.CMD )

        elif state.ID == self.STATE_MODE1.ID:
            # print( self.STATE_MODE1.TAG )
            next_cmd = self.runMODE1( self.CMD )
        elif state.ID == self.STATE_MODE2.ID:
            # print( self.STATE_MODE2.TAG )
            next_cmd = self.runMODE2( self.CMD )
        elif state.ID == self.STATE_MODE3.ID:
            # print( self.STATE_MODE3.TAG )
            next_cmd = self.runMODE3( self.CMD )
        elif state.ID == self.STATE_MODE4.ID:
            # print( self.STATE_MODE4.TAG )
            next_cmd = self.runMODE4( self.CMD )
        elif state.ID == self.STATE_MODE5.ID:
            # print( self.STATE_MODE5.TAG )
            next_cmd = self.runMODE5( self.CMD )
        elif state.ID == self.STATE_MODE6.ID:
            # print( self.STATE_MODE6.TAG )
            next_cmd = self.runMODE6( self.CMD )
        elif state.ID == self.STATE_MODE7.ID:
            # print( self.STATE_MODE7.TAG )
            next_cmd = self.runMODE7( self.CMD )

        else:
            # print( "DEFAULT STATE" )
            dmy = ""
            # next_cmd is null ..
        return next_cmd

    # overload this method by own needs ..
    def error(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd

    # overload this method by own needs ..
    def idle(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd

    # overload this method by own needs ..
    def runMODE1(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd

    # overload this method by own needs ..
    def runMODE2(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd

    # overload this method by own needs ..
    def runMODE3(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd

    # overload this method by own needs ..
    def runMODE4(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd

    # overload this method by own needs ..
    def runMODE5(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd

    # overload this method by own needs ..
    def runMODE6(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd

    # overload this method by own needs ..
    def runMODE7(self, PSSM_COMMAND):
        next_cmd = copy.copy(self.CMDS.NULL)
        return next_cmd
