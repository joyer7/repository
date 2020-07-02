"""
Created on Tue Apr 14 16:50:57 2020
@author: Shin Seok Rho
"""
# drelay 
import os
import json
save_file = "/fsrepo/stage/meta/drelay_current_repo_dict.json"

repo_dir_list = ['conda-forge', 'conda/pkgs/main', 'cran']
ostype_list = ['linux-64', 'linux-32', 'noarch', 'win-64']

repo_list_dict = {}
for repo in repo_dir_list:
    if repo =='cran':
        repo_list_dict["/fsrepo/{}".format(repo)] = os.listdir('/fsrepo/{}'.format(repo))
    else:    
      for ostype in ostype_list:
          repo_list_dict["/fsrepo/{}/{}".format(repo, ostype)] = os.listdir('/fsrepo/{}/{}'.format(repo, ostype))

with open(save_file, 'w') as f:
    json.dump(repo_list_dict, f, sort_keys=True, indent=4)
