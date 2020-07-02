#!/bin/bash

CRAN_DIR=/fsrepo/stage_trs

cd ${CRAN_DIR}
tar -zcvf cran/cran.tar.gz cran
split -b 1900m cran/cran.tar.gz "cran/cran.tar.gz.part-"
