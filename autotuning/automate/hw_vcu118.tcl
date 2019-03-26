# script to connect to the FPGA board

#start_gui
open_hw
connect_hw_server
#open_hw_target
#current_hw_device [get_hw_devices xcku115_0]
#refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xcku115_0] 0]
#close_hw_target {localhost:3121/xilinx_tcf/Xilinx/000013c0d16c01}
open_hw_target {localhost:3121/xilinx_tcf/Digilent/210308A62101}

# configure the FPGA
#set_property PROBES.FILE {/nfs/data41/rogl2082/FPGA/XCVU9P/vivado/ibert_231_28125_ex/ibert_231_28125_ex.runs/impl_1/example_ibert_231_28125.ltx} [get_hw_devices xcvu9p_0]
#set_property FULL_PROBES.FILE {/nfs/data41/rogl2082/FPGA/XCVU9P/vivado/ibert_231_28125_ex/ibert_231_28125_ex.runs/impl_1/example_ibert_231_28125.ltx} [get_hw_devices xcvu9p_0]
#set_property PROGRAM.FILE {/nfs/data41/rogl2082/FPGA/XCVU9P/vivado/ibert_231_28125_ex/ibert_231_28125_ex.runs/impl_1/example_ibert_231_28125.bit} [get_hw_devices xcvu9p_0]
set_property PROBES.FILE {/nfs/data41/rogl2082/FPGA/XCVU9P/vivado/ibert_233_1375_ex/ibert_233_1375_ex.runs/impl_1/example_ibert_233_1375.ltx} [get_hw_devices xcvu9p_0]
set_property FULL_PROBES.FILE {/nfs/data41/rogl2082/FPGA/XCVU9P/vivado/ibert_233_1375_ex/ibert_233_1375_ex.runs/impl_1/example_ibert_233_1375.ltx} [get_hw_devices xcvu9p_0]
set_property PROGRAM.FILE {/nfs/data41/rogl2082/FPGA/XCVU9P/vivado/ibert_233_1375_ex/ibert_233_1375_ex.runs/impl_1/example_ibert_233_1375.bit} [get_hw_devices xcvu9p_0]

program_hw_devices [get_hw_devices xcvu9p_0]
refresh_hw_device [lindex [get_hw_devices xcvu9p_0] 0]
