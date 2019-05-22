#!/usr/bin/env bash
#set -x

# Vivado installation
XIL="/nfs/data41/software/Xilinx/Vivado/2018.3/settings64.sh"


source $XIL

# open first and second Vivado instance and configure the FPGAs
trap 'kill -TERM $vivado1_pid' EXIT
vivado -mode tcl -source hw_yugevu1.tcl &
vivado1_pid=$!
sleep 30
trap 'kill -TERM $vivado2_pid' EXIT
vivado -mode tcl -source hw_vcu118.tcl &
vivado2_pid=$!
sleep 30

# run IBERT sweep
cd ..
python3 run.py
cd -

return 0
