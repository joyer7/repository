/!/bin/bash
CONDA_DIR=/fsrepo/stage_trs/conda/pkgs/main
OS_TYPE=noarch

cd ${CONDA_DIR}
tar -zcvf "${OS_TYPE}/${OS_TYPE}.tar.gz" ${OS_TYPE}
split -b 1900m "${OS_TYPE}/${OS_TYPE}.tar.gz" "${OS_TYPE}/${OS_TYPE}.tar.gz.part-"

