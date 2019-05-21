# script to connect to the FPGA board

open_hw
connect_hw_server
open_hw_target -quiet -xvc_url 128.138.133.229:2542
close_hw_target											;# Somehow it needs this two commands.
open_hw_target -verbose -xvc_url 128.138.133.229:2542	;# I do not know why.

# configure the FPGA
set_property PROBES.FILE {../../../../FPGA/XCVU080/vivado/ibert_129_28125_ex/ibert_129_28125_ex.runs/impl_1/example_ibert_129_28125.ltx} [get_hw_devices xcvu080_0]
set_property FULL_PROBES.FILE {../../../../FPGA/XCVU080/vivado/ibert_129_28125_ex/ibert_129_28125_ex.runs/impl_1/example_ibert_129_28125.ltx} [get_hw_devices xcvu080_0]
set_property PROGRAM.FILE {../../../../FPGA/XCVU080/vivado/ibert_129_28125_ex/ibert_129_28125_ex.runs/impl_1/example_ibert_129_28125.bit} [get_hw_devices xcvu080_0]

program_hw_devices [get_hw_devices xcvu080_0]
refresh_hw_device [lindex [get_hw_devices xcvu080_0] 0]
