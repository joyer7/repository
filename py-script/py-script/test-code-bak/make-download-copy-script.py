"""
Created on Tue Apr 14 16:50:57 2020
@author: hyeongyuy
"""
import sys
import os
import json
import time
import re


class MakeDownCopyScript(object):
    def __init__(self, argv):
        self.META_DIR = '/fsrepo/stage/meta'
        self.SAVE_SCRIPT_DIR = '/fsrepo/script/sh-script'

        self.CRAN_STAGE_REPO_DIR = '/fsrepo/stage/cran/cran.r-project.org'
        self.CONDA_STAGE_REPO_DIR = '/fsrepo/stage/conda/repo.continuum.io/pkgs/main'
        self.FORGE_STAGE_REPO_DIR = '/fsrepo/stage/conda-forge/conda.anaconda.org/conda-forge'

        self.CRAN_REPO_DIR = '/fsrepo/cran/cran.r-project.org'
        self.CONDA_REPO_DIR = '/fsrepo/conda/repo.continuum.io/pkgs/main'
        self.FORGE_REPO_DIR = '/fsrepo/conda-forge/conda.anaconda.org/conda-forge'

        self.unit_dict = {'': 1, 'K': 1024, 'M': 1024*1024}

        self.get_sys_args(argv)
        self.set_directories()
        

    def get_sys_args(self, argv):
        if argv[1] == 'cran':
            _, self.REPO_TYPE = argv
        else:
            _, self.REPO_TYPE, self.OS_TYPE = argv


    def set_directories(self):
        if self.REPO_TYPE == 'cran':
            self.META_FILE=os.path.join(self.META_DIR, '{}-repo.json'.format(self.REPO_TYPE))
            self.STAGE_REPO_DIR = self.CRAN_STAGE_REPO_DIR
            self.REPO_DIR = self.CRAN_REPO_DIR
            self.SAVE_SUMMARY_FILE =  os.path.join('/fsrepo/stage', 'summary-{}-repo.json'.format(self.REPO_TYPE))
            self.SAVE_SCRIPT_FILE =  '-{}-repo.sh'.format(self.REPO_TYPE)

        else:
            self.META_FILE=os.path.join(self.META_DIR, '{}-repo-{}.json'.format(self.REPO_TYPE, self.OS_TYPE))
            self.SAVE_SUMMARY_FILE =  os.path.join('/fsrepo/stage', 'summary-{}-repo-{}.json'.format(self.REPO_TYPE, self.OS_TYPE))
            self.SAVE_SCRIPT_FILE =  '-{}-repo-{}.sh'.format(self.REPO_TYPE, self.OS_TYPE)
              
            if self.REPO_TYPE == "conda":
                self.STAGE_REPO_DIR = os.path.join(self.CONDA_STAGE_REPO_DIR, self.OS_TYPE)
                self.REPO_DIR = os.path.join(self.CONDA_REPO_DIR, self.OS_TYPE)
            else:
                self.STAGE_REPO_DIR = os.path.join(self.FORGE_STAGE_REPO_DIR, self.OS_TYPE)
                self.REPO_DIR = os.path.join(self.FORGE_REPO_DIR, self.OS_TYPE)


        self.BASE_URL='https://' + '/'.join(self.REPO_DIR.split('/')[3:])

        if not os.path.exists(self.STAGE_REPO_DIR):
            os.makedirs(self.STAGE_REPO_DIR)
        if not os.path.exists(self.REPO_DIR):
            os.makedirs(self.REPO_DIR)



    def get_script(self):
        with open(self.META_FILE,'r') as read_file:
            meta_info = json.load(read_file)

        download_script = '#!/bin/bash\n'
        copy_script = '#!/bin/bash\n'
        summary = {'date':'Check new package time: ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                   'total_size': 0,
                   'num_total_files': 0,
                   'package_info':[]}

        if self.REPO_TYPE =='cran':
            meta_info = meta_info[list(meta_info.keys())[0]]
            for i, package in enumerate(meta_info.keys()):
                if not os.path.exists(self.STAGE_REPO_DIR+meta_info[package]['path']):
                    os.makedirs(self.STAGE_REPO_DIR+meta_info[package]['path'])
                if not os.path.exists(self.REPO_DIR+meta_info[package]['path']):
                    os.makedirs(self.REPO_DIR+meta_info[package]['path'])

                pack_name = os.path.join(meta_info[package]['path'], meta_info[package]['name'])
                url = self.BASE_URL + pack_name
                stage_repo_dir = self.STAGE_REPO_DIR + pack_name
                repo_dir = self.REPO_DIR + pack_name
                size_unit= meta_info[package]['size']
                resize = float(''.join(re.findall(r'\d+|\.',size_unit))) * self.unit_dict[re.findall('[A-Z]', size_unit.upper())[0]]
                
                if os.path.exists(os.path.join(self.REPO_DIR, package)):
                    print('[OK] %s'% meta_info[package]['name'])
                else:
                    print("[BAD] %s doesn't exists"%(stage_repo_dir))
                    download_script += 'wget --connect-timeout=2 --tries=3 -N {} -P {}/\n'.\
                        format(url, self.STAGE_REPO_DIR+meta_info[package]['path'])
                    copy_script += 'cp {} {}\n'.format(stage_repo_dir, repo_dir)
                    summary['total_size'] +=resize
                    summary['num_total_files'] +=1
                    summary['package_info'].append('{}, {}'.format(package, resize))
        else:
            for i, package in enumerate(meta_info['packages']):
                url = os.path.join(self.BASE_URL, package)
                stage_repo_dir = os.path.join(self.STAGE_REPO_DIR, package)
                repo_dir = os.path.join(self.REPO_DIR, package)
                package_size = int(meta_info['packages'][package]['size'])
                package_md5 = meta_info['packages'][package]['md5']

                # File Exists Check
                if os.path.exists(repo_dir):
                    real_size = os.stat(repo_dir).st_size

                    # File Size Check
                    if package_size == real_size:
                        real_md5 = os.popen('md5sum {}'.format(stage_repo_dir)).read().split(' ')[0]

                        # File Checksum Check
                        if package_md5 == real_md5:
                            print('[OK] %s'%package)
                        else:
                            print('[BAD] %s because of md5 checksum failure'%(package))
                            download_script += 'wget --connect-timeout=2 --tries=3 -N {} -P {}/\n'.format(url, self.STAGE_REPO_DIR)
                            copy_script += 'cp {} {}\n'.format(stage_repo_dir, repo_dir)
                            summary['total_size'] +=real_size
                            summary['num_total_files'] +=1
                            summary['package_info'].append('{}, {}'.format(package, real_size))
                    else:
                        print('[BAD] %s as The size of %s seems not ok (%d/%d)'%(package,package,real_size,package_size))
                        download_script += 'wget --connect-timeout=2 --tries=3 -N {} -P {}/\n'.format(url, self.STAGE_REPO_DIR)
                        copy_script += 'cp {} {}\n'.format(stage_repo_dir, repo_dir)
                        summary['total_size'] +=real_size
                        summary['num_total_files'] +=1
                        summary['package_info'].append('{}, {}'.format(package, real_size))
                else:
                    print("[BAD] %s as %s doesn't exists"%(package,package))
                    download_script += 'wget --connect-timeout=2 --tries=3 -N {} -P {}/\n'.format(url, self.STAGE_REPO_DIR)
                    copy_script += 'cp {} {}\n'.format(stage_repo_dir, repo_dir)
                    summary['total_size'] +=real_size
                    summary['num_total_files'] +=1
                    summary['package_info'].append('{}, {}'.format(package, real_size))
        return download_script, copy_script, summary


    def make_script(self):
        download_script, copy_script, summary = self.get_script()

        with open(os.path.join(self.SAVE_SCRIPT_DIR, 'download' + self.SAVE_SCRIPT_FILE), 'w+') as f:
            f.write(download_script)
        os.chmod(os.path.join(self.SAVE_SCRIPT_DIR, 'download' + self.SAVE_SCRIPT_FILE),0o755)

        with open(os.path.join(self.SAVE_SCRIPT_DIR, 'copy' + self.SAVE_SCRIPT_FILE), 'w+') as f:
            f.write(copy_script)
        os.chmod(os.path.join(self.SAVE_SCRIPT_DIR, 'copy' + self.SAVE_SCRIPT_FILE),0o755)

        with open(os.path.join(self.SAVE_SUMMARY_FILE), 'w') as f:
            json.dump(summary, f, sort_keys=True, indent=4)


if __name__ == '__main__':
    if sys.argv[-1] == 'get_meta':
        CRAN_URL = args.BASE_URL
        create_ist = get_cran_meta(args.BASE_URL, args.INIT_PATH)
        result = create_ist.get_result()

        with open(args.output, 'w') as f:
            json.dump(result, f, sort_keys=True, indent=4)

    else:
        createScriptObj = MakeDownCopyScript(sys.argv)
        createScriptObj.make_script()

