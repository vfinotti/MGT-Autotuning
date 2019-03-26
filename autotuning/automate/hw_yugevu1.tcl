# script to connect to the FPGA board

#start_gui
open_hw
connect_hw_server
#open_hw_target
#current_hw_device [get_hw_devices xcku115_0]
#refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xcku115_0] 0]
#close_hw_target
open_hw_target -verbose -xvc_url 128.138.133.229:2542
close_hw_target									;# Somehow it needs this two commands.
open_hw_target -xvc_url 128.138.133.229:2542	;# I do not know why.

# configure the FPGA
#set_property PROBES.FILE {/nfs/data41/rogl2082/FPGA/XCVU080/vivado/ibert_129_28125_ex/ibert_129_28125_ex.runs/impl_1/example_ibert_129_28125.ltx} [get_hw_devices xcvu080_0]
#set_property FULL_PROBES.FILE {/nfs/data41/rogl2082/FPGA/XCVU080/vivado/ibert_129_28125_ex/ibert_129_28125_ex.runs/impl_1/example_ibert_129_28125.ltx} [get_hw_devices xcvu080_0]
#set_property PROGRAM.FILE {/nfs/data41/rogl2082/FPGA/XCVU080/vivado/ibert_129_28125_ex/ibert_129_28125_ex.runs/impl_1/example_ibert_129_28125.bit} [get_hw_devices xcvu080_0]
set_property PROBES.FILE {/nfs/data41/rogl2082/FPGA/XCVU080/vivado/ibert_124_125_126_1375_ex/ibert_124_125_126_1375_ex.runs/impl_1/example_ibert_124_125_126_1375.ltx} [get_hw_devices xcvu080_0]
set_property FULL_PROBES.FILE {/nfs/data41/rogl2082/FPGA/XCVU080/vivado/ibert_124_125_126_1375_ex/ibert_124_125_126_1375_ex.runs/impl_1/example_ibert_124_125_126_1375.ltx} [get_hw_devices xcvu080_0]
set_property PROGRAM.FILE {/nfs/data41/rogl2082/FPGA/XCVU080/vivado/ibert_124_125_126_1375_ex/ibert_124_125_126_1375_ex.runs/impl_1/example_ibert_124_125_126_1375.bit} [get_hw_devices xcvu080_0]

program_hw_devices [get_hw_devices xcvu080_0]
refresh_hw_device [lindex [get_hw_devices xcvu080_0] 0]
