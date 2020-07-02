#!/bin/bash

echo "--------------------------------------------"
echo "● Repository Manager           "
echo "● Editor                                    "
echo "  - Shin Seok Rho           "
echo "  - joyer@kolon.com, injoyer@yonsei.ac.kr   "
echo "--------------------------------------------"


echo -n "Do you want to start to make meta  <y/n > "
read -i Y  input
#echo "You said <${input}>"
if [[ "$input" == "y" || "$input" == "Y" ]]; then
        echo "-------------------------"
        echo "-- OK! Let's Go!"
        echo "-------------------------"
else
        echo "-------------------------"
        echo "-- Bye bye          "
        echo "-------------------------"
        exit
fi

DIR=/fsrepo/stage/meta
n_files="$(ls -l ${DIR}/ |grep ^-| wc -l)"

if [ "$n_files" -ge 1 ];
then
    mkdir "${DIR}/metabak/meta.$(date '+%Y%m%d')"
    mv ${DIR}/*.json "${DIR}/metabak/meta.$(date '+%Y%m%d')"
fi

echo "Create ${DIR}/forge-repo-linux-64.json file"
wget -O ${DIR}/forge-repo-linux-64.json --connect-timeout=2 --tries=3 -N https://conda.anaconda.org/conda-forge/linux-64/repodata.json

echo "Create ${DIR}/forge-repo-linux-32.json file"
wget -O ${DIR}/forge-repo-linux-32.json --connect-timeout=2 --tries=3 -N https://conda.anaconda.org/conda-forge/linux-32/repodata.json

echo "Create ${DIR}/forge-repo-noarch.json file"
wget -O ${DIR}/forge-repo-noarch.json --connect-timeout=2 --tries=3 -N https://conda.anaconda.org/conda-forge/noarch/repodata.json

echo "Create ${DIR}/forge-repo-win-64.json file"
wget -O ${DIR}/forge-repo-win-64.json --connect-timeout=2 --tries=3 -N https://conda.anaconda.org/conda-forge/win-64/repodata.json

echo "Create ${DIR}/conda-repo-linux-64.json file"
wget -O ${DIR}/conda-repo-linux-64.json --connect-timeout=2 --tries=3 -N https://repo.anaconda.com/pkgs/main/linux-64/repodata.json

echo "Create ${DIR}/conda-repo-linux-32.json file"
wget -O ${DIR}/conda-repo-linux-32.json --connect-timeout=2 --tries=3 -N https://repo.anaconda.com/pkgs/main/linux-32/repodata.json

echo "Create ${DIR}/conda-repo-noarch.json file"
wget -O ${DIR}/conda-repo-noarch.json --connect-timeout=2 --tries=3 -N https://repo.anaconda.com/pkgs/main/noarch/repodata.json

echo "Create ${DIR}/conda-repo-win-64.json file"
wget -O ${DIR}/conda-repo-win-64.json --connect-timeout=2 --tries=3 -N https://repo.anaconda.com/pkgs/main/win-64/repodata.json

echo "Create ${DIR}/cran-repo.json file"
python3 /fsrepo/script/py-script/make-cran-meta.py


