## cool Python Serial State Machine

### Introduction
Client and Server implementation for sending to ARDUINO & PYTHON (using both class [PSSM_CLient](https://github.com/graetz23/coolPythonSerialStateMachine/blob/master/coolPSSM.py)) and receiving from ARDUINO (using [cool Arduino Serial State Machine](https://github.com/graetz23/coolArduinoSerialStateMachine) commands, states, and data via serial console.

### Usage

1. Flash the project: [Arduino Serial State Temperature Cable Probe](https://github.com/graetz23/ArduinoSerialStateTempCableProbe).
  If you do not have some Negative Temperature Coefficient (NTC) cable probes, do not worry, open analog inputs are always drifting will deliever _true_ random data.
2. Plug arduino to USB port and be sure by: _ls /dev_ that there is _/dev/ttyACM0_ listed,
3. Clone or download this project, and type: _python run.display_
4. To kill all threads, take a new terminal and: _ps ux | grep python_ and _kill -9 <PID>_

### Remarks

This project is written in **python 2.7**

I have written an [arduino](https://www.arduino.cc/) library as the _mirrow_ project: [cool Arduino Serial State Machine](https://github.com/graetz23/coolArduinoSerialStateMachine), where arduino is acting as a server for driving or / and processing sensor / actor / .. data and sending it.

Everything was coded using:

  - [**python 2.7**](https://www.python.org/),
  - [**atom**](https://atom.io/) editor,
  - [**Gnome**](https://www.gnome.org/) as window manager,
  - and [**debian**](https://www.debian.org/) GNU/Linux.

have fun :-)

## ChangeLog

**version 20200404**
  - **Rewritten arduino's method based style to some python's object-oritend style**:
    - **PSSM_Client works fine** to comand and request arduino,
      - I used [Arduino Serial State Temp Cable Probe](https://github.com/graetz23/ArduinoSerialStateTempCableProbe) for running this example.
      - **reading** arduino's **answer** in a **seperate** speedy **thread**,
      - **saving answers in style** of **memento**; keeping last always available
    - **PSSM_Server**, which is the equivalent to [cool Arduino Serial State Machine](https://github.com/graetz23/coolArduinoSerialStateMachine):
      - Not debugged yet, while have to setup a _dummy serial console_, etc.
      - ** no necessary; to follow ..**

**version 20200401**
  - created repository [coolPythonSerialStateMachine](https://github.com/graetz23/coolPythonSerialStateMachine.git) on github.
