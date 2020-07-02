#!/bin/bash

SH_DIR=/fsrepo/script/sh-script
CRAN_DIR=/fsrepo/stage_trs

for fn in `ls ${CRAN_DIR}/cran/cran.tar.gz.part-* | awk '{print $1}'`
do
    echo "=$fn="
    ${SH_DIR}/trans/transfile.sh "$fn" "$fn" dportal2 kolon rwxr-xr-x
done

${SH_DIR}/trans/transfile.sh "${SH_DIR}/dportal-copy-cran-repo.sh" "${SH_DIR}/dportal-copy-cran-repo.sh" dportal2 kolon rwxr-xr-x

