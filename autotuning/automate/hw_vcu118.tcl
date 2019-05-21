# script to connect to the FPGA board

open_hw
connect_hw_server
open_hw_target {localhost:3121/xilinx_tcf/Digilent/210308A62101}

# configure the FPGA
set_property PROBES.FILE {../../../../FPGA/XCVU9P/vivado/ibert_231_28125_ex/ibert_231_28125_ex.runs/impl_1/example_ibert_231_28125.ltx} [get_hw_devices xcvu9p_0]
set_property FULL_PROBES.FILE {../../../../FPGA/XCVU9P/vivado/ibert_231_28125_ex/ibert_231_28125_ex.runs/impl_1/example_ibert_231_28125.ltx} [get_hw_devices xcvu9p_0]
set_property PROGRAM.FILE {../../../../FPGA/XCVU9P/vivado/ibert_231_28125_ex/ibert_231_28125_ex.runs/impl_1/example_ibert_231_28125.bit} [get_hw_devices xcvu9p_0]

program_hw_devices [get_hw_devices xcvu9p_0]
refresh_hw_device [lindex [get_hw_devices xcvu9p_0] 0]
