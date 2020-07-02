"""
Created on Tue Apr 14 16:50:57 2020
@author: hyeongyuy
"""
import sys
import os
import json
import time
import re
from bs4 import BeautifulSoup
import requests



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



class GetCranMeta(object):
    def __init__(self):
        self.BASE_URL = 'https://cran.r-project.org'
        #self.INIT_PATH = '/src/contrib'
        self.INIT_PATH = '/src/contrib/4.0.0/Recommended'
        self.OUTPUT = '/fsrepo/stage/meta/cran-repo.json'
        self.file_dict = {}
        self.start_time = time.time()
        self.connection_error_count = 0
        self.count = 0
        print("====== Strart Time ====== ", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

    def get_source(self, url):
        try:
            with requests.Session() as session:
                source = BeautifulSoup(requests.get(url).text, 'html.parser')
        except requests.exceptions.ConnectionError as e:
            print('ConnectionError :\n{}\n\nReconnecting...'.format(e))
            self.connection_error_count += 1
            time.sleep(3)
            with requests.Session() as session:
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                source = BeautifulSoup(requests.get(url).text, 'html.parser')
        return source


    def sep_dir_file(self, base_url, files = {}):
        def set_static_len(string, length, char='='):
            return string + char*(length - len(string))

        self.count += 1

        print("Please wait a minute\nbase url: {}".format(base_url))
        source = self.get_source(base_url)
        trs = source.find_all("table")[0].find_all('tr')
        path = source.find_all("h1")[0].text.strip().replace('Index of ','')
        outstr = ("{}. PATH: {}\n" .format(self.count, path))

        print(set_static_len(outstr, 100))

        folder = {}

        for i, tr in enumerate(trs):
            try:
                lib_name = tr.select('tr > td > a')[0].get('href');date,date,size_unit = "","",""

                if tr.select('tr > td > img')[0].get('alt') =='[DIR]':
                    continue

                elif '.tar.gz' in lib_name:
                    date, size_unit = [r.text.strip() for r in tr.select('tr > td') if '"right"' in str(r)]
                    files[os.path.join(path, lib_name.replace('.tar.gz',''))] = {'name':lib_name, 'date':date, 'size':size_unit, 'path' : path}

                print('[Meta OK] file info: {} {} {} {} {}'.\
                      format(set_static_len(str(i+1), 3, ' '), set_static_len(lib_name,30, ' '), \
                             set_static_len(date, 15, ' '), set_static_len(size_unit, 4, ' '), path))
            except IndexError:
                pass

        return folder, files


    def rec_folder(self, url):
        subfd, subfl = self.sep_dir_file(url)

        folder_dir = url.replace(self.BASE_URL, '')
        folderlist = [i for i in folder_dir.split('/') if i != '']

        if len(subfd) != 0:
            for url in subfd.values():
                self.rec_folder(url)
                #print("This is folder")
        else:
            folder_dict = {folder_dir: subfl}
            self.file_dict =  dict(self.file_dict, **folder_dict)

    def get_cran_meta(self):
        try:
            self.rec_folder(self.BASE_URL + self.INIT_PATH)
        except Exception as ex:
            print('Exception:\n{}'.format(ex))
            return self.file_dict

        print('\nCompleted\n{}Process summary\n{}\nTime: {}\nConnection erorr count: {}\n# of directories: {}'.\
              format("="*50, "="*50, time.time() - self.start_time,\
                     self.connection_error_count, \
                     len(self.file_dict)))
                     
                     
        
        with open(self.OUTPUT, 'w') as f:
            json.dump(self.file_dict, f, sort_keys=True, indent=4)

            

if __name__ == '__main__':
    print(sys.argv[-1])
    if sys.argv[-1] == 'get_cran_meta':
        create_inst = GetCranMeta()
        create_inst.get_cran_meta()
            
    else:
        createScriptObj = MakeDownCopyScript(sys.argv)
        createScriptObj.make_script()

