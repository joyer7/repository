
import os
import json

load_file="list.json"
only_drelay_file = "only_dreally_file.json"
only_dportal2_file = "only_dportal2_file.json"

only_drelay_dict ={}
only_dportal2_dict = {}


with open(load_file, 'r') as f:
    repo_list_dict = json.load(f)

for dir_ in repo_list_dict.keys():
    dportal2_repo = os.listdir(dir_)
    delay_repo = repo_list_dict[dir_]
    
    only_drelay_dict[dict_]= list(set(drelay_repo) - set(dportal2_repo))
    only_dportal2_dict[dict_]= list(set(dportal2_repo) - set(drelay_repo))


with open(only_drelay_file, 'w') as f:
    json.dump(only_delay_dict, f,sort_keys=True, indent=4)

with open(only_dportla2_file, 'w') as f:
    json.dump(only_dportal2_dict, f, sort_keys=True, ident4)