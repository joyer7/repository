#!/bin/bash

echo "Make script start!"
echo "Output list: [Download libarary .sh file(use wget cmd), Summary downloaded .json file,  Copy repo .sh file(use cp cmd)]"

python3 /fsrepo/script/py-script/make-download-copy-script.py forge linux-64
#python3 /fsrepo/script/py-script/make-download-copy-script.py forge linux-32
python3 /fsrepo/script/py-script/make-download-copy-script.py forge noarch
python3 /fsrepo/script/py-script/make-download-copy-script.py forge win-64
python3 /fsrepo/script/py-script/make-download-copy-script.py conda linux-64
#python3 /fsrepo/script/py-script/make-download-copy-script.py conda linux-32
python3 /fsrepo/script/py-script/make-download-copy-script.py conda noarch
python3 /fsrepo/script/py-script/make-download-copy-script.py conda win-64
python3 /fsrepo/script/py-script/make-download-copy-script.py cran

echo "========================================================="
echo "Make script Complete!, Please check summary info"
echo "Summary files: /fsrepo/stage/summary/summary-*.json"

