#!/bin/bash

echo "Compress & Split(resize=1,900m)"
echo "Compress Start"

/fsrepo/script/sh-script/compress/compress-forge-repo-linux-64.sh
/fsrepo/script/sh-script/compress/compress-forge-repo-linux-32.sh
/fsrepo/script/sh-script/compress/compress-forge-repo-noarch.sh
/fsrepo/script/sh-script/compress/compress-forge-repo-win-64.sh
/fsrepo/script/sh-script/compress/compress-conda-repo-linux-64.sh
/fsrepo/script/sh-script/compress/compress-conda-repo-linux-32.sh
/fsrepo/script/sh-script/compress/compress-conda-repo-noarch.sh
/fsrepo/script/sh-script/compress/compress-conda-repo-win-64.sh
/fsrepo/script/sh-script/compress/compress-cran-repo.sh


