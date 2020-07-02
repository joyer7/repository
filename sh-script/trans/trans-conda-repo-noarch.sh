#!/bin/bash

SH_DIR=/fsrepo/script/sh-script
CONDA_DIR=/fsrepo/stage_trs/conda/pkgs/main
OS_TYPE=noarch

for fn in `ls ${CONDA_DIR}/${OS_TYPE}/${OS_TYPE}.tar.gz.part-* | awk '{print $1}'`
do
    echo "=$fn="
    ${SH_DIR}/trans/transfile.sh "$fn" "$fn" dportal2 kolon rwxr-xr-x
done

${SH_DIR}/trans/transfile.sh "${SH_DIR}/dportal-copy-conda-repo-${OS_TYPE}.sh" "${SH_DIR}/dportal-copy-conda-repo-${OS_TYPE}.sh" dportal2 kolon rwxr-xr-x

