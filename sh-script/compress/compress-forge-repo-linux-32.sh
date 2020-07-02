#!/bin/bash

GE_DIR=/fsrepo/stage_trs/conda-forge
OS_TYPE=linux-32

cd ${FORGE_DIR}
tar -zcvf "${OS_TYPE}/${OS_TYPE}.tar.gz" ${OS_TYPE}
split -b 1900m "${OS_TYPE}/${OS_TYPE}.tar.gz" "${OS_TYPE}/${OS_TYPE}.tar.gz.part-"

