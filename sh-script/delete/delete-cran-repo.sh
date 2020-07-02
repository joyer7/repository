#!/bin/bash

CRAN_DIR=/fsrepo/stage_trs/cran


echo -n "Do you want to delete ${CRAN_DIR}/*  <y/n > "
read -i Y  input
#echo "You said <${input}>"
if [[ "$input" == "y" || "$input" == "Y" ]]; then
    echo "Delete all file"
    rm -rf ${CRAN_DIR}/*
else
    echo "Not deleted"
fi


