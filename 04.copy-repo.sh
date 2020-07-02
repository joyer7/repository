#!/bin/bash

echo "Copy stage -> currenct library & stage -> stage_trs"
echo "Copy Start"

/fsrepo/script/sh-script/copy-forge-repo-linux-64.sh
/fsrepo/script/sh-script/copy-forge-repo-linux-32.sh
/fsrepo/script/sh-script/copy-forge-repo-noarch.sh
/fsrepo/script/sh-script/copy-forge-repo-win-64.sh
/fsrepo/script/sh-script/copy-conda-repo-linux-64.sh
/fsrepo/script/sh-script/copy-conda-repo-linux-32.sh
/fsrepo/script/sh-script/copy-conda-repo-noarch.sh
/fsrepo/script/sh-script/copy-conda-repo-win-64.sh
/fsrepo/script/sh-script/copy-cran-repo.sh
