#!/bin/bash

FORGE_DIR=/fsrepo/stage_trs/conda-forge
OS_TYPE=/linux-32

echo -n "Do you want to delete ${FORGE_DIR}${OS_TYPE}/*  <y/n > "
read -i Y  input
#echo "You said <${input}>"
if [[ "$input" == "y" || "$input" == "Y" ]]; then
    echo "Delete all file"
    rm -rf ${FORGE_DIR}${OS_TYPE}/*
else
    echo "Not deleted"
fi



