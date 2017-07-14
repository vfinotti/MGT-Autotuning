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

def write_result_csv(f, TXDIFFSWING, TXPRE, TXPOST, RXTERM, scan_area):
    f.write(i
            + "," +  TXDIFFSWING
            + "," +  TXPRE
            + "," +  TXPOST
            + "," +  scan_area
            + "\n")

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
desired_area = config.getint('test','desired_area')
include_all_results = config.getboolean('test','include_all_results')

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

                    transm.reset_all_gth_tx()
                    rcv.reset_all_gth_rx()

                    print("------ Transceiver - " + mgt[mgt_idx])
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
                            write_result_csv(f, i, j, k, l, scan_area)
                            if int(float(scan_area)) > int(float(best_area)):
                                best_area = scan_area
                                best_diff = i
                                best_txpre = j
                                best_txpost = k
                                best_rx = l

                    if (link == "0" or int(err,16) != 0) and include_all_results:
                        write_result_csv(f, i, j, k, l, "0")

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
    write_result_csv(f, best_diff, best_txpre, best_txpost, best_rx, best_area)
    f.close()

    print("End of " + mgt[mgt_idx])

transm.close_hw()
rcv.close_hw()
