"""
Created on Tue Apr 14 16:50:57 2020
@author: Shin Seok Rho
"""
import os
import json
import time
import re
from bs4 import BeautifulSoup
import requests


class GetCranMeta(object):
    def __init__(self):
        self.BASE_URL = 'https://cran.r-project.org'
        self.INIT_PATH = '/src/contrib'
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
    create_inst = GetCranMeta()
    create_inst.get_cran_meta()


