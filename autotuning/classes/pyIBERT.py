#-----------------------------------------------------------------------------
# Title      : Xilinx IBERT Interface Class
# Project    :
#-----------------------------------------------------------------------------
# File       : pyIBERT.py
# Author     : Vitor Finotti Ferreira
# Company    :
# Created    : 2017-07-12
# Last update: 2017-07-12
# Standard   : Python 3.4
#-----------------------------------------------------------------------------
# Description:
#
# Implements a interface to communicate with Xilinx IBERT
#
#-----------------------------------------------------------------------------
# Copyright (c) 2017 Vitor Finotti Ferreira
#-----------------------------------------------------------------------------
# Revisions  :
# Date        Version  Author          Description
# 2017-Jul-12 1.0      vfinotti        Created
#-----------------------------------------------------------------------------


from classes.XilinxTCL import XilinxTCL
import time

class pyIBERT(XilinxTCL):
  def __init__(self, server_addr, server_port, target_name, target_freq):
    XilinxTCL.__init__(self)
    self.server_url = server_addr + ":" + server_port
    self.target_name = target_name
    self.target_freq = target_freq
    self.connect()

  def connect(self):
    self.create()

    self.sendCommand("open_hw")
    self.sendCommand("connect_hw_server -url " + self.server_url)
    time.sleep(3) # required delay to refresh information (xilinx bug)
    self.sendCommand("disconnect_hw_server " + self.server_url)
    self.sendCommand("connect_hw_server -url "+ self.server_url)
    if self.target_freq == '0': # for xvc
      self.sendCommand("open_hw_target -verbose -xvc_url "
                       + self.target_name)
    else:
      self.sendCommand("current_hw_target [get_hw_targets */xilinx_tcf/*"
                       + self.target_name + "*]")
      self.sendCommand("set_property PARAM.FREQUENCY " + self.target_freq
                       + " [get_hw_targets */xilinx_tcf/*"
                       + self.target_name + "*]")
      self.sendCommand("open_hw_target")
    self.sendCommand("current_hw_device [lindex [get_hw_devices] 0]")
    self.sendCommand("refresh_hw_device -update_hw_probes false [lindex [get_hw_devices] 0]")

  def source(self, path):
    self.sendCommand("source " + path)

  def scan_create(self, name, obj):
    self.sendCommand("set " + name + " [create_hw_sio_scan -description {" + name + "} 2d_full_eye  [lindex [" + obj + "] 0 ]]")

  def scan_set_all(self, vert_align, hor_align, dwell):
    self.sendCommand("set_property VERTICAL_INCREMENT " + str(vert_align) + " [get_hw_sio_scans]")
    self.sendCommand("set_property HORIZONTAL_INCREMENT " + str(hor_align) + " [get_hw_sio_scans]")
    self.sendCommand("set_property DWELL_BER " + str(dwell) + " [get_hw_sio_scans]")

  def scan_run_all(self):
    self.sendCommand("foreach s [get_hw_sio_scans] {\n    run_hw_sio_scan $s \n    wait_on_hw_sio_scan $s}")

  def scan_remove_all(self):
    self.sendCommand("remove_hw_sio_scan [get_hw_sio_scans]")

  def set_property(self, prop, value, obj):
#    print("set_property " + prop + " {" + str(value) + "} [" + obj + "]")
    self.sendCommand("set_property " + prop + " {" + str(value) + "} [" + obj + "]")
#    print("commit_hw_sio" + " [" + obj + "]")
    self.sendCommand("commit_hw_sio" + " [" + obj + "]")

  def get_property(self, prop, obj):
    return self.sendQuery("get_property " + prop + " [" + obj + "]")

  def reset_sio_link_error(self, obj):
    self.set_property("LOGIC.MGT_ERRCNT_RESET_CTRL", "1", obj)
    self.set_property("LOGIC.MGT_ERRCNT_RESET_CTRL", "0", obj)

  def refresh_hw_sio(self, obj):
    self.sendCommand("refresh_hw_sio [" + obj + "]")

  def reset_all_gth_tx(self):
    self.sendCommand("set_property PORT.GTTXRESET 1 [get_hw_sio_links "+
                     "-of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
    self.sendCommand("commit_hw_sio [get_hw_sio_links -of_objects "+
                     "[get_hw_sio_linkgroups {LINKGROUP_0}]]")
    self.sendCommand("set_property PORT.GTTXRESET 0 [get_hw_sio_links "+
                     "-of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
    self.sendCommand("commit_hw_sio [get_hw_sio_links -of_objects "+
                     "[get_hw_sio_linkgroups {LINKGROUP_0}]]")

  def reset_all_gth_rx(self):
    self.sendCommand("set_property PORT.GTRXRESET 1 [get_hw_sio_links "+
                     "-of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
    self.sendCommand("commit_hw_sio [get_hw_sio_links -of_objects "+
                     "[get_hw_sio_linkgroups {LINKGROUP_0}]]")
    self.sendCommand("set_property PORT.GTRXRESET 0 [get_hw_sio_links "+
                     "-of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]")
    self.sendCommand("commit_hw_sio [get_hw_sio_links -of_objects "+
                     "[get_hw_sio_linkgroups {LINKGROUP_0}]]")

  def close_hw(self):
    self.sendCommand("close_hw")
    self.terminate()
