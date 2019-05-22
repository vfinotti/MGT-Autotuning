# script to connect to the FPGA board

open_hw
connect_hw_server
open_hw_target -xvc_url yugevu2:2542

# configure the FPGA
set_property PROBES.FILE {../../../../firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_231_ex/ibert_1625_231_ex.runs/impl_1/example_ibert_1625_231.ltx} [get_hw_devices xcvu080_0]
set_property FULL_PROBES.FILE {../../../../firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_231_ex/ibert_1625_231_ex.runs/impl_1/example_ibert_1625_231.ltx} [get_hw_devices xcvu080_0]
set_property PROGRAM.FILE {../../../../firmware/TrackletProject/YUGE/BoardTest/FPGA/vivado/ibert_1625_231_ex/ibert_1625_231_ex.runs/impl_1/example_ibert_1625_231.bit} [get_hw_devices xcvu080_0]
program_hw_devices [get_hw_devices xcvu080_0]
refresh_hw_device [lindex [get_hw_devices xcvu080_0] 0]
