#-----------------------------------------------------------------------------
# Title      : Autotuning System for Xilinx MGTs
# Project    :
#-----------------------------------------------------------------------------
# File       : run.py
# Author     : Vitor Finotti Ferreira
# Company    :
# Created    : 2017-07-12
# Last update: 2017-07-12
# Standard   : Python 3.4
#-----------------------------------------------------------------------------
# Description:
#
# Autotuning script for the KC705 GTX transceivers
#
#-----------------------------------------------------------------------------
# Copyright (c) 2017 Vitor Finotti Ferreira
#-----------------------------------------------------------------------------
# Revisions  :
# Date        Version  Author          Description
# 2017-Jul-12 1.0      vfinotti        Created
#-----------------------------------------------------------------------------


from classes.pyIBERT import pyIBERT
import time
import os
from configparser import SafeConfigParser

# Functions
def create_dir(dir):
    # checks if data subdirectory exists. If not, create it.
    os.makedirs(os.getcwd() + "/" + os.path.dirname(dir), exist_ok=True)

def format_to_list(data):
    data = data.replace(",\n",",")
    data = data.split(",")
    return data

# Load init
config = SafeConfigParser()
config.read('config.ini')
server0_addr = config.get('hw_server','server0_addr')
server0_port = config.get('hw_server','server0_port')
target0_name = config.get('hw_server','target0_name')
target0_freq = config.get('hw_server','target0_freq')
server1_addr = config.get('hw_server','server1_addr')
server1_port = config.get('hw_server','server1_port')
target1_name = config.get('hw_server','target1_name')
target1_freq = config.get('hw_server','target1_freq')
mgt = config.get('mgt_parameters','mgt')
TXDIFFSWING = config.get('mgt_parameters','TXDIFFSWING')
TXPOST = config.get('mgt_parameters','TXPOST')
TXPRE = config.get('mgt_parameters','TXPRE')
RXTERM = config.get('mgt_parameters','RXTERM')
tcl_dir = config.get('test','tcl_dir')
tcl_transm_name = config.get('test','tcl_transm_name')
tcl_rcv_name = config.get('test','tcl_rcv_name')
results_dir = config.get('test','results_dir')
results_name = config.get('test','results_name')
desired_area = config.get('test','desired_area')

mgt = format_to_list(mgt)
TXDIFFSWING = format_to_list(TXDIFFSWING)
TXPOST = format_to_list(TXPOST)
TXPRE = format_to_list(TXPRE)
RXTERM = format_to_list(RXTERM)

# Main script
print("----------------------------------------------------------------------")
print("Creating Instance 0")
rcv = pyIBERT(server0_addr,server0_port,target0_name,target0_freq)
print("Creating Instance 1")
transm = pyIBERT(server1_addr,server1_port,target1_name,target1_freq)

rcv.source("./" + tcl_dir + tcl_rcv_name + ".tcl")
transm.source("./" + tcl_dir + tcl_transm_name + ".tcl")

create_dir(results_dir)

for mgt_idx in range(len(mgt)):

    f = open("./" + results_dir + results_name + mgt[mgt_idx] + ".csv","w")
    f.write("TXDIFFSWING"
            + "," + "TXPRE"
            + "," + "TXPOST"
            + "," + "RXTERM"
            + "," + "Open Area"
            + "\n")
    obj = "get_hw_sio_links *MGT_" + mgt[mgt_idx] + "/RX"

    rcv.scan_remove_all()
    transm.scan_remove_all()

    iter = 0

    best_area = "-1"
    best_diff = TXDIFFSWING[0]
    best_rx = RXTERM[0]
    best_txpost = TXPOST[0]
    best_txpre = TXPRE[0]

    for i in TXDIFFSWING[::4]:
        transm.set_property("TXDIFFSWING", i, obj)
        for j in TXPRE[::4]:
            transm.set_property("TXPRE", j, obj)
            for k in TXPOST[::4]:
                transm.set_property("TXPOST", k, obj)
                for l in RXTERM[::1]:
                    rcv.set_property("RXTERM", l, obj)

                    transm.sendCommand("set_property PORT.GTTXRESET 1 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
                    transm.sendCommand("commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
                    transm.sendCommand("set_property PORT.GTTXRESET 0 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
                    transm.sendCommand("commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
                    rcv.sendCommand("set_property PORT.GTRXRESET 1 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
                    rcv.sendCommand("commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
                    rcv.sendCommand("set_property PORT.GTRXRESET 0 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
                    rcv.sendCommand("commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")

                    print("------ DFE_8gbps - " + mgt[mgt_idx])
                    print("------ Iter: " + str(iter))
                    print(iter)
                    iter = iter+1

                    rcv.reset_sio_link_error(obj)
                    rcv.refresh_hw_sio(obj)
                    time.sleep(6) # parameters are not instantly refreshed
                    link = rcv.get_property("LOGIC.LINK", obj)

                    if link == "1":
                        err = rcv.get_property("LOGIC.ERRBIT_COUNT", obj)

                        if int(err,16) == 0: # convert str hex to int

                            rcv.scan_create("xil_scan", obj)
                            rcv.scan_set_all("6", "6", "1e-9")
                            rcv.scan_run_all()

                            scan_area = rcv.get_property("Open_Area", "get_hw_sio_scan")
                            #scan_ber = rcv.get_property("RX_BER", obj)
                            rcv.scan_remove_all()
                            f.write(i
                                    + "," +  j
                                    + "," +  k
                                    + "," +  l
                                    + "," +  scan_area
                                    + "\n")

                            if int(float(scan_area)) > int(float(best_area)):
                                best_area = scan_area
                                best_diff = i
                                best_txpre = j
                                best_txpost = k
                                best_rx = l
                    if int(float(best_area)) > desired_area:
                        break
                if int(float(best_area)) > desired_area:
                    break
            if int(float(best_area)) > desired_area:
                break
        if int(float(best_area)) > desired_area:
            break



    transm.set_property("TXDIFFSWING", best_diff, obj)
    transm.set_property("TXPRE", best_txpre, obj)
    transm.set_property("TXPOST", best_txpost, obj)
    rcv.set_property("RXTERM", best_rx, obj)

    print("exit main()")

    f.write("------------BEST------------\n")
    f.write(best_diff
            + "," +  best_txpre
            + "," +  best_txpost
            + "," +  best_rx
            + "," +  best_area
            + "\n")

    f.close()

    print("End of " + mgt[mgt_idx])

rcv.sendCommand("close_hw")
transm.sendCommand("close_hw")

rcv.terminate()
transm.terminate()
