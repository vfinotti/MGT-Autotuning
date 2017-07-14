# Autotuning System for Xilinx MGTs

## Overview
In order to have a stable link, sometimes it is required to tune transmitter and
receiver so attenuations and inferences can be compensated. Although Xilinx
provides tools for doing this automatically, this is only possible in
applications where the boards are in the same JTAG chain. Applications where the
transmitter and receiver are in different boards (and in most cases in
different JTAG chains) would demand a manual tuning of the channels. In order
to optimize this process, some scripts were designed to permit an automatic
tuning of the links. This is done by two classes:

- **XilinxTCL.py**, which implements an interface of commands between python
3 and Xilinx tcl language

- **pyIBERT.py**, which uses XilinxTCL.py to implement specific commands related to
Xilinx IBERT (Integrated Bit Error Ratio Tester) tests

Basically, a python script uses the two classes to communicate with Vivado and
to set the desired values on transmitter and receiver. The performance of the
link is mesured by the same script, which checks if the channel is stable and
its performance. Different test configurations and performance evaluation
conditions may be used.
