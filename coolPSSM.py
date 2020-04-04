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
            time.sleep(0.01) # obvious useless ??

    # Decoupling from speedy method; while REQUEST / RESPONSE things, MEMENTO
    # carries ALWAYS the received RESPONSE for the REQUEST, if the CLIENT is
    # NOT too FAST with reading put the MEMENTO; try to SLEEP a little bit on
    # CLIENT side.
    def getMemento(self):
        return self.MEMENTO

# Super Class for SERIAL Messages in PSSM
class PSSM_Message:

    ID = None # for iterating members; do NOT CHANGE the order
    TAG = None # for iterating members; do NOT CHANGE the order
    DATA = None # for iterating members; do NOT CHANGE the order

    def __init__(self):
        pass

    def hasID(self):
        answer = False
        if self.ID != None:
            answer = True
        return answer

    def hasTAG(self):
        answer = False
        if self.TAG != None:
            answer = True
        return answer

    def hasDATA(self):
        answer = False
        if self.DATA != None:
            answer = True
        return answer

    # this is the STYLE to send from PYTHON to ARDUINO
    def genID(self):
        msg = ""
        if self.hasID() :
            msg = "<" + str(self.ID) + ">"
        return msg

    # this is the STYLE to send from ARDUINO & PYTHON to PYTHON
    def genTAG(self):
        msg = ""
        if self.hasTAG() :
            msg = "<" + str(self.TAG) + "/>"
        return msg

    # this is the STYLE to send from ARDUINO & PYTHON to PYTHON
    def genDATA(self):
        msg = ""
        if  self.hasTAG( ) and hasDATA():
            msg = "<" + self.TAG + ">" + str(self.DATA) + "</" + self.TAG + ">"
        return msg

# representing a COMMAND by ID (for arduino) and STR (for python)
class PSSM_Command(PSSM_Message):

    def __init__(self, id, tag):
        PSSM_Message( ) # obvious useless
        self.ID = id
        self.TAG = tag
        self.DATA = None #obvious useless

    # COPY CONSTRUCTOR in python ~8>
    def COPY(self):
        return copy.copy(self)

# representing a STATE by ID (for arduino) and STR (for python)
class PSSM_State(PSSM_Message):

    def __init__(self, id, tag):
        PSSM_Message( ) # obvious useless
        self.ID = id
        self.TAG = tag
        self.DATA = None #obvious useless

    # COPY CONSTRUCTOR in python ~8>
    def COPY(self):
        return copy.copy(self)

# This is to send data; however here is NO numerical ID while it is not forseen
# to send data from PYTHON to ARDUINO
class PSSM_Data(PSSM_Message):

    def __init__(self, tag, data):
        PSSM_Message( ) # obvious useless
        self.ID = None #obvious useless
        self.TAG = tag
        self.DATA = data

    # COPY CONSTRUCTOR in python ~8>
    def COPY(self):
        return copy.copy(self)

# representing an itertable set of all COMMANDs that ARDUINO / PYTHON can use to
# intercommunication. ARDUINO receives IDs, while PYTHON receives STRINGS. The
# IDs are SYNC to the ITERATOR stuff of python; keep this!
class PSSM_Commands:

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
        self.NULL = PSSM_Command(  0, "NULL" ) # NULL or NO COMMAND; is handled as a CMD
        self.SNA  = PSSM_Command(  1," SNA" ) # service not available (SNA); go error state
        self.PING = PSSM_Command(  2," PING" ) # send a PING and try get a PONG response
        self.PONG = PSSM_Command(  3," PONG" ) # send a PONG for a PING receive
        self.AKNW = PSSM_Command(  4," AKNW" ) # ACKNOWLEDGE a received command
        self.RUN  = PSSM_Command(  5," RUN" ) # signal to WAIT to CLIENT or SERVER
        self.WAIT = PSSM_Command(  6," WAIT" ) # signal to WAIT to CLIENT or SERVER
        self.EVNT = PSSM_Command(  7," EVNT" ) # signal an EVENT to CLIENT or SERVER
        self.DONE = PSSM_Command(  8," DONE" ) # send a STOP to CLIENT or SERVER
        self.STOP = PSSM_Command(  9," STOP" ) # send a STOP to CLIENT or SERVER
        self.STAT = PSSM_Command( 10, "STAT" ) # request the STATUS of CLIENT or SERVER
        self.RMD1 = PSSM_Command( 11, "RMD1" ) # let arduino do something while in run MODE 1
        self.RMD2 = PSSM_Command( 12, "RMD2" ) # let arduino do something while in run MODE 2
        self.RMD3 = PSSM_Command( 13, "RMD3" ) # let arduino do something while in run MODE 3
        self.RMD4 = PSSM_Command( 14, "RMD4" ) # let arduino do something while in run MODE 4
        self.RMD5 = PSSM_Command( 15, "RMD5" ) # let arduino do something while in run MODE 5
        self.RMD6 = PSSM_Command( 16, "RMD6" ) # let arduino do something while in run MODE 6
        self.RMD7 = PSSM_Command( 17, "RMD7" ) # let arduino do something while in run MODE 7
        self.CNCT = PSSM_Command( 18, "CNCT" ) # obvious useless yet
        self.DCNT = PSSM_Command( 19, "DCNT" ) # obvious useless yet

# The STATES that ARDUINO / PYTHON can state while running. PYTHON sends IDs to
# ARDUINO, while ARDUINO sends STRINGS to PYTHON; however STATEs are only SENT
# as STRINGS in case of an ID based STAT (status) COMMAND request.
class PSSM_States:

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
        self.ERROR = PSSM_State( 0, "ERROR " ) # arduino is in ERROR state
        self.IDLNG = PSSM_State( 1, "IDLNG" ) # arduino is IDILING around
        # run MODEs; MODE1, MODE2, .., MODE7
        self.MODE1 = PSSM_State( 11, "MODE1" ) # arduino is processing MODE 1
        self.MODE2 = PSSM_State( 12, "MODE2" ) # arduino is processing MODE 2
        self.MODE3 = PSSM_State( 13, "MODE3" ) # arduino is processing MODE 3
        self.MODE4 = PSSM_State( 14, "MODE4" ) # arduino is processing MODE 4
        self.MODE5 = PSSM_State( 15, "MODE5" ) # arduino is processing MODE 5
        self.MODE6 = PSSM_State( 16, "MODE6" ) # arduino is processing MODE 6
        self.MODE7 = PSSM_State( 17, "MODE7" ) # arduino is processing MODE 7

# TOOL for exploding read COMMANDs baking PSSM_State & PSSM_Command objects ..
class PSSM_XML:

    CMDS = None # obvious useless in python

    STATES = None # obvious useless in python

    def __init__(self):

        self.CMDS   = PSSM_Commands() # PROTOTYPEs that can be iterated

        self.STATES = PSSM_States() # PROTOTYPEs that can be iterated

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

# Utilizes the serial console, especially the reading method for receiving
# IDs and / or STRINGs. However, the reading methods should be always threaded.
class PSSM_Serial:

    MEMENTO = None

    SER = None # serial console set to NULL

    # Constructor
    def __init__(self, port, baud):

        MEMENTO = None # obvious useless

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
        message = None # we read STRINGS; by an example
        chars = b"" # read BYTES first
        if self.isOpen(): # obvious useless ??
            while self.SER.inWaiting( ):
                chars += self.SER.read_until( '>' ) # read single byte
        if len( chars ) > 2:
            message = str( chars ) # transform BYTES to STRING
            self.MEMENTO = message # obvious useless
            # print( message ) # DEBUG print out; delete later
        return message

    # send from PYTHON to ARDUINO
    def writeID(self, pssm_Msg):
        isWritten = False
        if self.isOpen( ) :
            if isinstance( pssm_Msg, PSSM_Message ) :
                if pssm_Msg.hasID( ) :
                    print( pssm_Msg.genID( ) ) # DEBUG print out; delete later
                    self.SER.write( pssm_Msg.genID( ) ) # send ID to ARDUINO
                    isWritten = True
        return isWritten

    # send from ARDUINO & PYTHON to PYTHON
    def writeTAG(self, pssm_Msg): # send ID _NOT_ STR to arduino
        isWritten = False
        if self.isOpen( ) :
            if isinstance( pssm_Msg, PSSM_Message ) :
                if pssm_Msg.hasTAG( ) :
                    print( pssm_Msg.genTAG( ) ) # DEBUG print out; delete later
                    self.SER.write( pssm_Msg.genTAG( ) ) # send ID _NOT_ STR to arduino
                    isWritten = True
        return isWritten

    # send from ARDUINO & PYTHON to PYTHON
    def writeDATA(self, pssm_Msg): # send ID _NOT_ STR to arduino
        isWritten = False
        if self.isOpen( ) :
            if isinstance( pssm_Msg, PSSM_Message ) :
                if pssm_Msg.hasDATA( ) :
                    print( pssm_Msg.genDATA( ) ) # DEBUG print out; delete later
                    self.SER.write( pssm_Msg.genDATA( ) ) # send ID _NOT_ STR to arduino
                    isWritten = True
        return isWritten

    # return the LAST RECEIVED Answer of ARDUINO; works well while we are
    # in CHALLANGING / RESPONDING COMMUNICATION and having SLOW MOVING PHYSICS
    # on ARDUINO SIDE
    def getMEMENTO(self):
        return self.MEMENTO

class PSSM_Client():

    CMDS = None # obvious useless in python

    STATES = None # obvious useless in python

    SERIAL = None # obvious useless in python

    THREAD_READING = None # obvious useless in python

    # Constructor
    def __init__(self, port, baud):

        self.CMDS   = PSSM_Commands( ) # PROTOTYPEs that can be iterated

        self.STATES = PSSM_States( ) # PROTOTYPEs that can be iterated

        self.SERIAL = PSSM_Serial(port, baud) # GETTIN high on SERIAL

        self.threadStopFlag = Event()
        self.THREAD_READING = PSSM_Serial_Thread(self.threadStopFlag, self)
        self.THREAD_READING.start()

    # send from PYTHON to ARDUINO
    def writeID(self, pssm_Msg):
        return self.SERIAL.writeID( pssm_Msg )

    # send from ARDUINO & PYTHON to PYTHON
    def writeTAG(self, pssm_Msg):
        return self.SERIAL.writeTAG( pssm_Msg )

    # send from ARDUINO & PYTHON to PYTHON
    def writeDATA(self, pssm_Msg):
        return self.SERIAL.writeDATA( pssm_Msg )

    # get the ANSWER (MEMENTO) that ARDUINO has SENT BACK TO LAST REQUEST
    def getANSWER(self):
        return self.SERIAL.getMEMENTO( )

class PSSM_Server:

    CMDS = None # obvious useless in python

    STATES = None # obvious useless in python

    SERIAL = None # obvious useless in python

    THREAD_READING = None # obvious useless in python

    CMD = None

    STATE = None

    # Constructor
    def __init__(self, port, baud):

        self.CMDS   = PSSM_Commands( ) # PROTOTYPEs that can be iterated

        self.STATES = PSSM_States( ) # PROTOTYPEs that can be iterated

        self.SERIAL = PSSM_Serial(port, baud) # GETTIN high on SERIAL

        self.CMD = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE

        self.STATE = self.STATES.IDLNG.COPY( ) # start up in IDLNG state

        self.threadStopFlag = Event()
        self.THREAD_READING = PSSM_Serial_Thread(self.threadStopFlag, self)
        self.THREAD_READING.start()

    # Let's keep ARDUINO STYLE in python
    def setup(self):
        pass

    # Let's keep ARDUINO STYLE in python
    def loop(self):

        #while True:
        read = self.THREAD_READING.READ # TODO THIS is not SYNC YET - do MEMENTO

        if len(read) > 0  :
            # TODO convert the the STRING COMMAND to match an OBJECT
            print( read )

        self.CMD = self.CMDS.IDLNG.COPY( ) # DEBUG print out; delete later

        self.STATE = self.process_Command(self.CMD)
        print( "process_Command" + " - " + "next_State:   " + str(self.STATE.ID) + " " + self.STATE.TAG ) # DEBUG print out; delete later

        self.CMD = self.process_State(self.STATE) # next COMMAND is not used here .. is stored by memeber var
        print( "process_State" + "   - " + "next_Command: " + str(self.CMD.ID) + " " + self.CMD.TAG ) # DEBUG print out; delete later

        print( " " ) # DEBUG print out; delete later
        time.sleep(1) # DEBUG print out; delete later

    def process_Command(self, cmd):

        self.CMD = cmd # obvious useless

        next_state = self.STATE.COPY( ) # next state is same state

        # if elif else block goes here
        if cmd.ID == self.CMDS.SNA.ID:
            print( self.CMDS.SNA.TAG ) # DEBUG print out; delete later
            next_state = self.STATES.ERROR.COPY( ) # switch

        elif cmd.ID == self.CMDS.PING.ID:
            print( self.CMDS.PING.TAG ) # DEBUG print out; delete later
            if self.STATE.ID == self.STATES.ERROR.ID:  # move out of error state
                next_state = self.STATES.IDLNG.COPY( )  # switch
            else: # obvious useless
                next_state = self.STATE.COPY( )
            self.SERIAL.writeTAG( self.CMDS.PONG )

        elif cmd.ID == self.CMDS.PONG.ID:
            print( self.CMDS.PONG.TAG ) # DEBUG print out; delete later
            if self.STATE.ID == self.STATES.ERROR.ID: # move out of error state
                next_state = self.STATES.IDLNG.COPY( )  # switch
            else: # obvious useless
                next_state = self.STATE.COPY( )
            self.SERIAL.writeTAG( self.CMDS.PING )

        elif cmd.ID == self.CMDS.AKNW.ID:
            print( self.CMDS.AKNW.TAG ) # DEBUG print out; delete later
            next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.RUN.ID:
            print( self.CMDS.RUN.TAG ) # DEBUG print out; delete later
            if self.STATE.ID == self.STATES.MODE1.ID: # just ACKNOWLEDGE
                next_state = self.STATE.COPY( )
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE2.ID: # just ACKNOWLEDGE
                next_state = self.STATE.COPY( )
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE3.ID: # just ACKNOWLEDGE
                next_state = self.STATE.COPY( )
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE4.ID: # just ACKNOWLEDGE
                next_state = self.STATE.COPY( )
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE5.ID: # just ACKNOWLEDGE
                next_state = self.STATE.COPY( )
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE6.ID: # just ACKNOWLEDGE
                next_state = self.STATE.COPY( )
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE7.ID: # just ACKNOWLEDGE
                next_state = self.STATE.COPY( )
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            else: # obvious useless
                next_state = self.STATE.COPY( )

        elif cmd.ID == self.CMDS.STOP.ID:
            print( self.CMDS.STOP.TAG ) # DEBUG print out; delete later
            if self.STATE.ID == self.STATES.MODE1.ID: # move to IDLNG
                next_state = self.STATES.IDLNG.COPY( ) # switch
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE2.ID: # move to IDLNG
                next_state = self.STATES.IDLNG.COPY( ) # switch
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE3.ID: # move to IDLNG
                next_state = self.STATES.IDLNG.COPY( ) # switch
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE4.ID: # move to IDLNG
                next_state = self.STATES.IDLNG.COPY( )  # switch
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE5.ID: # move to IDLNG
                next_state = self.STATES.IDLNG.COPY( ) # switch
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE6.ID: # move to IDLNG
                next_state = self.STATES.IDLNG.COPY( ) # switch
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            elif self.STATE.ID == self.STATES.MODE7.ID: # move to IDLNG
                next_state = self.STATES.IDLNG.COPY( ) # switch
                self.SERIAL.writeTAG( self.CMDS.AKNW )
            else: # obvious useless
                next_state = self.STATE.COPY( )

        elif cmd.ID == self.CMDS.WAIT.ID:
            print( self.CMDS.WAIT.TAG ) # DEBUG print out; delete later
            next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.EVENT.ID:
            print( self.CMDS.EVENT.TAG ) # DEBUG print out; delete later
            next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.DONE.ID:
            print( self.CMDS.DONE.TAG ) # DEBUG print out; delete later
            next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.STATUS.ID:
            print( self.CMDS.STATUS.TAG ) # DEBUG print out; delete later
            next_state = self.STATE.COPY( ) # obvious useless
            self.SERIAL.writeTAG( self.STATE )

        elif cmd.ID == self.CMDS.CNCT.ID:
            print( self.CMDS.CNCT.TAG ) # DEBUG print out; delete later
            next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.DCNT.ID:
            print( self.CMDS.DCNT.TAG ) # DEBUG print out; delete later
            next_state = self.STATE.COPY( ) # obvious useless

        # RUN MODEs ..

        elif cmd.ID == self.CMDS.RMD1.ID:
            print( self.ASSM_CMDS.RMD1.TAG ) # DEBUG print out; delete later
            if self.STATE.ID != self.STATES.ERROR.ID:
                print( self.STATES.MODE1.TAG ) # DEBUG print out; delete later
                next_state = self.STATES.MODE1.COPY( ) # switch
            else:
                next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.RMD2.ID:
            print( self.ASSM_CMDS.RMD2.TAG ) # DEBUG print out; delete later
            if self.STATE.ID != self.STATES.ERROR.ID:
                print( self.STATES.MODE2.TAG ) # DEBUG print out; delete later
                next_state = self.STATES.MODE2.COPY( ) # switch
            else:
                next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.RMD3.ID:
            print( self.ASSM_CMDS.RMD3.TAG ) # DEBUG print out; delete later
            if self.STATE.ID != self.STATES.ERROR.ID:
                print( self.STATES.MODE3.TAG ) # DEBUG print out; delete later
                next_state = self.STATES.MODE3.COPY( ) # switch
            else:
                next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.RMD4.ID:
            print( self.ASSM_CMDS.RMD4.TAG ) # DEBUG print out; delete later
            if self.STATE.ID != self.STATES.ERROR.ID:
                print( self.STATES.MODE4.TAG ) # DEBUG print out; delete later
                next_state = self.STATES.MODE4.COPY( ) # switch
            else:
                next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.RMD5.ID:
            print( self.ASSM_CMDS.RMD5.TAG ) # DEBUG print out; delete later
            if self.STATE.ID != self.STATES.ERROR.ID:
                print( self.STATES.MODE5.TAG ) # DEBUG print out; delete later
                next_state = self.STATES.MODE5.COPY( ) # switch
            else:
                next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.RMD6.ID:
            print( self.ASSM_CMDS.RMD6.TAG ) # DEBUG print out; delete later
            if self.STATE.ID != self.STATES.ERROR.ID:
                print( self.STATES.MODE6.TAG ) # DEBUG print out; delete later
                next_state = self.STATES.MODE6.COPY( ) # switch
            else:
                next_state = self.STATE.COPY( ) # obvious useless

        elif cmd.ID == self.CMDS.RMD7.ID:
            print( self.ASSM_CMDS.RMD7.TAG ) # DEBUG print out; delete later
            if self.STATE.ID != self.STATES.ERROR.ID:
                print( self.STATES.MODE7.TAG ) # DEBUG print out; delete later
                next_state = self.STATES.MODE7.COPY( ) # switch
            else:
                next_state = self.STATE.COPY( ) # obvious useless

        else:
            # print( self.CMDS.NULL.TAG )
            next_state = self.STATE.COPY( )  # obvious useless

        return next_state

    def process_State(self, state):

        self.STATE = state # obvious useless

        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE

        if state.ID == self.STATES.ERROR.ID:
            print( self.STATES.ERROR.TAG ) # DEBUG print out; delete later
            next_cmd = self.error( self.CMD )

        elif state.ID == self.STATES.IDLNG.ID:
            print( self.STATES.IDLNG.TAG ) # DEBUG print out; delete later
            next_cmd = self.idle( self.CMD )

        elif state.ID == self.STATES.MODE1.ID:
            print( self.STATES.MODE1.TAG ) # DEBUG print out; delete later
            next_cmd = self.runMODE1( self.CMD )
        elif state.ID == self.STATES.MODE2.ID:
            print( self.STATES.MODE2.TAG ) # DEBUG print out; delete later
            next_cmd = self.runMODE2( self.CMD )
        elif state.ID == self.STATES.MODE3.ID:
            print( self.STATES.MODE3.TAG ) # DEBUG print out; delete later
            next_cmd = self.runMODE3( self.CMD )
        elif state.ID == self.STATES.MODE4.ID:
            print( self.STATES.MODE4.TAG ) # DEBUG print out; delete later
            next_cmd = self.runMODE4( self.CMD )
        elif state.ID == self.STATES.MODE5.ID:
            print( self.STATES.MODE5.TAG ) # DEBUG print out; delete later
            next_cmd = self.runMODE5( self.CMD )
        elif state.ID == self.STATES.MODE6.ID:
            print( self.STATES.MODE6.TAG ) # DEBUG print out; delete later
            next_cmd = self.runMODE6( self.CMD )
        elif state.ID == self.STATES.MODE7.ID:
            print( self.STATES.MODE7.TAG ) # DEBUG print out; delete later
            next_cmd = self.runMODE7( self.CMD )

        else:
            # print( "DEFAULT" ) # DEBUG print out; delete later
            next_cmd = copy.copy(self.CMDS.NULL) # no new COMMAND from this STATE

        return next_cmd

    # Following methods can be extended by own code ..

    def error(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd

    def idle(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd

    def runMODE1(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd

    def runMODE2(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd

    def runMODE3(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd

    def runMODE4(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd

    def runMODE5(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd

    def runMODE6(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd

    def runMODE7(self, PSSM_Command):
        next_cmd = self.CMDS.NULL.COPY( ) # no new COMMAND from this STATE
        #
        # own code to process goes here
        #
        return next_cmd
