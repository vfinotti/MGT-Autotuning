# script to connect to the FPGA board

#start_gui
open_hw
connect_hw_server
#open_hw_target
#current_hw_device [get_hw_devices xcku115_0]
#refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xcku115_0] 0]
#close_hw_target {localhost:3121/xilinx_tcf/Xilinx/000013c0d16c01}
open_hw_target -xvc_url yugevu2:2542

# configure the FPGA
#set_property PROBES.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_VUx_125_ex/ibert_VUx_125_ex.runs/impl_1/example_ibert_VUx_125.ltx} [get_hw_devices xcvu080_0]
#set_property FULL_PROBES.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_VUx_125_ex/ibert_VUx_125_ex.runs/impl_1/example_ibert_VUx_125.ltx} [get_hw_devices xcvu080_0]
#set_property PROGRAM.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_VUx_125_ex/ibert_VUx_125_ex.runs/impl_1/example_ibert_VUx_125.bit} [get_hw_devices xcvu080_0]
#set_property PROBES.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_125_ex/ibert_1625_125_ex.runs/impl_1/example_ibert_1625_125.ltx} [get_hw_devices xcvu080_0]
#set_property FULL_PROBES.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_125_ex/ibert_1625_125_ex.runs/impl_1/example_ibert_1625_125.ltx} [get_hw_devices xcvu080_0]
#set_property PROGRAM.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_125_ex/ibert_1625_125_ex.runs/impl_1/example_ibert_1625_125.bit} [get_hw_devices xcvu080_0]
set_property PROBES.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_231_ex/ibert_1625_231_ex.runs/impl_1/example_ibert_1625_231.ltx} [get_hw_devices xcvu080_0]
set_property FULL_PROBES.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_231_ex/ibert_1625_231_ex.runs/impl_1/example_ibert_1625_231.ltx} [get_hw_devices xcvu080_0]
set_property PROGRAM.FILE {/home/rglein/git/firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_231_ex/ibert_1625_231_ex.runs/impl_1/example_ibert_1625_231.bit} [get_hw_devices xcvu080_0]
program_hw_devices [get_hw_devices xcvu080_0]
refresh_hw_device [lindex [get_hw_devices xcvu080_0] 0]
