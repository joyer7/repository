#!/bin/bash

CONDA_DIR=/fsrepo/stage_trs/conda/pkgs/main
OS_TYPE=/win-32

echo -n "Do you want to delete ${CONDA_DIR}${OS_TYPE}/*  <y/n > "
read -i Y  input
#echo "You said <${input}>"
if [[ "$input" == "y" || "$input" == "Y" ]]; then
    echo "Delete all file"
    rm -rf ${CONDA_DIR}${OS_TYPE}/*
else
    echo "Not deleted"
fi





