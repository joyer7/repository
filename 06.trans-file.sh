#!/bin/bash

echo "Transfort list: New library compressed file, Copy script file, Summary info file"
echo "Transfort Start"

/fsrepo/script/sh-script/trans/trans-forge-repo-linux-64.sh
/fsrepo/script/sh-script/trans/trans-forge-repo-linux-32.sh
/fsrepo/script/sh-script/trans/trans-forge-repo-noarch.sh
/fsrepo/script/sh-script/trans/trans-forge-repo-win-64.sh
/fsrepo/script/sh-script/trans/trans-conda-repo-linux-64.sh
/fsrepo/script/sh-script/trans/trans-conda-repo-linux-32.sh
/fsrepo/script/sh-script/trans/trans-conda-repo-noarch.sh
/fsrepo/script/sh-script/trans/trans-conda-repo-win-64.sh
/fsrepo/script/sh-script/trans/trans-cran-repo.sh

/fsrepo/script/sh-script/trans/trans-meta-json.sh
/fsrepo/script/sh-script/trans/trans-summary-json.sh

