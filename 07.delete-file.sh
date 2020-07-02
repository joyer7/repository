#!/bin/bash

echo -n "Do you want to delete /fsrepo/stage_trs/[cran,conda,conda-forge]/*  <y/n > "
read -i Y  input

#echo "You said <${input}>"
if [[ "$input" == "y" || "$input" == "Y" ]]; then
    echo "Delete all file"
    /fsrepo/script/sh-script/delete/delete-conda-repo-linux-64.sh
    /fsrepo/script/sh-script/delete/delete-conda-repo-linux-32.sh
    /fsrepo/script/sh-script/delete/delete-conda-repo-noarch.sh
    /fsrepo/script/sh-script/delete/delete-conda-repo-win-64.sh
    /fsrepo/script/sh-script/delete/delete-forge-repo-linux-64.sh
    /fsrepo/script/sh-script/delete/delete-forge-repo-linux-32.sh
    /fsrepo/script/sh-script/delete/delete-forge-repo-noarch.sh
    /fsrepo/script/sh-script/delete/delete-forge-repo-win-64.sh
    /fsrepo/script/sh-script/delete/delete-cran-repo.sh
else
    echo "Not deleted"
fi






