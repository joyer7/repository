#!/bin/bash

SH_DIR=/fsrepo/script/sh-script
META_DIR=/fsrepo/stage/meta

for fn in `ls ${META_DIR}/*-repo*.json | awk '{print $1}'`
do
    echo "=$fn="
    ${SH_DIR}/trans/transfile.sh "$fn" "$fn" dportal2 kolon rwxr-xr-x
done


