#!/bin/bash

echo "--------------------------------------------"
echo "● Repository Manager           "
echo "● Editor                                    "
echo "  - Shin Seok Rho           "
echo "  - joyer@kolon.com, injoyer@yonsei.ac.kr   "
echo "--------------------------------------------"


echo "========================================================="
echo "= 1 Get Meta                                            ="
echo "=  - cran : httsp://cran.r-project.com/src/contrib      ="                       
echo "=  - conda : https://repo.anaconda.com/pkgs/main        ="
echo "=  - forge : https://conda.anaconda.org/conda-forge     ="
echo "========================================================="
/fsrepo/script/01.make-meta.sh

echo "========================================================="
echo "= 2. Check Meta & Local Repo                            ="
echo "=  - Make Download Script                               ="
echo "=  - Make Copy Script                                   ="
echo "=  - Meta : Local (lastest)                             ="
echo "=  - Local Repo : /fsrepo/stage/meta                    ="
echo "========================================================="
/fsrepo/script/02.make-download-copy-script.sh

echo "========================================================="
echo "= 3. Download Libraries                                 ="
echo "=  - stage : /fsrepo/stage/[cran|conda|forge]           =" 
echo "========================================================="
/fsrepo/script/03.download-repo.sh

echo "========================================================="
echo "= 4. Copy Libraries                                     ="
echo "=  - /fsrepo/stage/[cran|conda|forge] -> fsrepo/        ="
echo "========================================================="
/fsrepo/script/04.copy-repo.sh

echo "========================================================="
echo "= 5. Zip & split                                        ="
echo "========================================================="
/fsrepo/script/05.compress-split.sh

echo "========================================================="
echo "= 6. Tranfort file                                      ="
echo "=  - files : cran.tar.gz*                               ="
echo "=  - from  : drelay  :/fsrepo/stage_trs/cran/           ="
echo "=  - to    : dportal2:/fsrepo/stage_trs/cran/           ="
echo "========================================================="
/fsrepo/script/06.trans-file.sh

echo "========================================================"
echo "= 7. Delete                                            ="
echo "=  - /fsrepo/stage_trs/[conda,conda-forge,cran]/*      ="
echo "========================================================"
/fsrepo/script/07.delete-file.sh

echo "========================================================"
echo "= 8. Make current drelay repo list                     ="
echo "========================================================"
/fsrepo/script/08.check-current-repolist.sh

echo "========================================================"
echo "= 9. Completed                                         ="
echo "========================================================"

