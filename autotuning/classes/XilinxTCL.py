#-----------------------------------------------------------------------------
# Title      : Xilinx TCL commands
# Project    :
#-----------------------------------------------------------------------------
# File       : XilinxTCL.py
# Author     : Vitor Finotti Ferreira
# Company    :
# Created    : 2017-07-12
# Last update: 2017-07-12
# Standard   : Python 3.4
#-----------------------------------------------------------------------------
# Description:
#
# Defines a class that creates a subprocess of Vivado for communicating with
# it, implementing methods to send commands and do queries.
#
#-----------------------------------------------------------------------------
# Copyright (c) 2017 Vitor Finotti Ferreira
#-----------------------------------------------------------------------------
# Revisions  :
# Date        Version  Author          Description
# 2017-Jul-12 1.0      vfinotti        Created
#-----------------------------------------------------------------------------

import subprocess

class XilinxTCL(object):

  def __init__(self):
    #self.executable = "/opt/Xilinx/Vivado/2017.2/bin/vivado" # vivado bin file
                                                             # path
    self.executable = "vivado" # vivado bin file
    self.boundaryString = "PROC_BOUNDARY"
    self.boundaryCommand = bytearray("puts {0}\n".format(self.boundaryString),
                                     "ascii")

  def create(self):
    self.proc = subprocess.Popen([self.executable, "-mode","tcl"],
                                                 stdin=subprocess.PIPE,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT)
    self.writeBoundaryCommand()
    while(True):
      stdoutLine = self.proc.stdout.readline().decode()
      if (self.boundaryString in stdoutLine):
        break
      else:
        print(stdoutLine.rstrip())

  def terminate(self):
    self.proc.terminate()

  def writeBoundaryCommand(self):
    self.proc.stdin.write(self.boundaryCommand)
    self.proc.stdin.flush()

  def writeCommand(self, line):
    """ Send command without checking the output of the process. This is an
    intermediary command and should not be used directly to communicate with the
    process """
    command = bytearray("{0}\n".format(line), "ascii")
    self.proc.stdin.write(command)
    self.writeBoundaryCommand()

  def sendCommand(self, line, verbose = True):
    """ Send command to the process and wait the boundaryString, indicating it
    has been processed """
    self.writeCommand(line)
    while(True):
      stdoutLine = self.proc.stdout.readline().decode()
      if (self.boundaryString in stdoutLine):
        break
      else:
        if (verbose == True):
          print(stdoutLine.rstrip())

  def sendQuery(self, line, verbose = True):
    """ Send command, wait for boundaryString and return the last valid line
    returned from the process """
    self.writeCommand("puts [" + line + "]")
    stdoutLine_0 = self.proc.stdout.readline().decode()
    stdoutLine_1 = stdoutLine_0
    while(True):
      stdoutLine_1 = stdoutLine_0 # storing last value of output
      stdoutLine_0 = self.proc.stdout.readline().decode() # most recent output
      if (self.boundaryString in stdoutLine_0):
        if (verbose == True):
          print(stdoutLine_1.rstrip())
        return stdoutLine_1.rstrip()
      else:
        if (verbose == True):
          print(stdoutLine_0.rstrip())
