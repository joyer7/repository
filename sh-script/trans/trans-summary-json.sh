#!/bin/bash

SH_DIR=/fsrepo/script/sh-script
SUM_SH_DIR=/fsrepo/stage/summary

for fn in `ls ${SUM_SH_DIR}/*.json | awk '{print $1}'`
do
    echo "=$fn="
    ${SH_DIR}/trans/transfile.sh "$fn" "$fn" dportal2 kolon rwxr-xr-x
done

