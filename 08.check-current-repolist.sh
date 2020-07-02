#!/bin/bash
META_DIR=/fsrepo/stage/meta

echo "Make current repo list(save : /fsrepo/stage/meta/drelay_current_repo_dict.json)"
python3 /fsrepo/script/py-script/make-current-repo.py

echo "Transfort file: /fsrepo/stage/meta/drelay_current_repo_dict.json"
/fsrepo/script/sh-script/trans/transfile.sh "${META_DIR}/drelay_current_repo_dict.json" "${META_DIR}/drelay_current_repo_dict.json" dportal2 kolon rwxr-xr-x

