# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:50:57 2020
@author: hyeongyuy
"""
from bs4 import BeautifulSoup
import requests
import json
import time
import re
import argparse
import os
import sys
import subprocess

#set args
parser = argparse.ArgumentParser('')
parser.add_argument('--BASE_URL', dest ='BASE_URL', default = 'https://cran.r-project.org')
parser.add_argument('--INIT_PATH', dest ='INIT_PATH', default = '/src/contrib/')
parser.add_argument('--output', dest ='output', default = '/fsrepo/stage/meta/cran-repo.json')
parser.add_argument('--out_unit', dest ='out_unit', default = 'gb')
parser.add_argument('--connection_error_sleep_time', dest='connection_error_sleep_time',\
                    default = 3, type=int, help='sleep time(s) until reconnection when ConnectionError occurs')
args = parser.parse_args()
#print(args)


class recur_url(object):
    def __init__(self, BASE_URL,INIT_PATH):
        self.BASE_URL = BASE_URL
        self.INIT_PATH = INIT_PATH
        self.file_dict = {}
        self.start_time = time.time()
        self.connection_error_count = 0
        self.unit_dict = {'': 1, 'K': 1024, 'M': 1024*1024}
        self.out_unit_dict = {'gb': 1024*1024*1024, 'mb':1024*1024, 'kb':1024, '': 1}
        self.count = 0
        self.total_size = 0
        self.total_N_files = 0
        self.notAllow = ["00Archieve","1.4.0","1.4.1","1.5.0","1.5.1","1.6.0","1.6.1","1.6.2","1.7.0","1.7.1","1.8.0", \
        "1.8.1","1.9.0","1.9.1","1.9.1-patched","2.0-patched","2.0.0","2.0.1","2.0.1-patched","2.1-patched","2.1.0-patched", \
        "2.1.1","2.2-patched", "2.2.0-patched", "2.2.0","2.2.1", "2.3-patched", "2.3.0", "2.3.1", "2.4-patched", "2.4.0", "2.4.1", \
        "2.5.0", "2.5-patched","2.5.1","2.6-patched", "2.6-patehed", "2.6.0", "2.6.1", "2.6.2", "2.7-patched", "2.7.0", "2.7.1", "2.7.2", \
        "2.8.0", "2.8-patched", "2.8.1","2.9-patched","2.9.0","2.9.1","2.9.2","2.10-pathced","2.10.0","2.10.1","2.11-patched","2.11.0", \
        "2.11.1","2.12-patched", "2.12.0", "2.12.1", "2.12.2" \
        ]
        print("====== Strart Time ====== ", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))

    def get_source(self, url):
        try:
            #print("network -->")
            with requests.Session() as session:
                source = BeautifulSoup(requests.get(url).text, 'html.parser')
        except requests.exceptions.ConnectionError as e:
            print('ConnectionError :\n{}\n\nReconnecting...'.format(e))
            self.connection_error_count += 1
            time.sleep(args.connection_error_sleep_time)
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

        print("Please wait a minute")
        source = self.get_source(base_url)
        trs = source.find_all("table")[0].find_all('tr')
        path = source.find_all("h1")[0].text.strip().replace('Index of ','')
        outstr = ("{}. PATH: {}" .format(self.count, path))
        
        print(set_static_len(outstr, 100))

        folder = {}
        
        for i, tr in enumerate(trs):
            #if i < 2: continue
            #-------------------------------------------------------
            # File Name, Date, Size
            try:
                lib_name = tr.select('tr > td > a')[0].get('href');date,date,size_unit = "","",""

                if tr.select('tr > td > img')[0].get('alt') =='[DIR]':
                    continue
                    #new_url = base_url + lib_name
                    #folder[lib_name.replace('/', '')] = new_url

                elif '.tar.gz' in lib_name:
                    date, size_unit = [r.text.strip() for r in tr.select('tr > td') if '"right"' in str(r)]
                    files[path + lib_name.replace('.tar.gz','')] = {'name':lib_name, 'date':date, 'size':size_unit, 'path' : path}
                    
                    resize = float(''.join(re.findall(r'\d+|\.',size_unit))) * self.unit_dict[re.findall('[A-Z]', size_unit.upper())[0]]
                    self.total_size += resize
                    self.total_N_files += 1

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

    def get_result(self):
        try:
            self.rec_folder(self.BASE_URL + self.INIT_PATH)
        except Exception as ex:
            print('Exception:\n{}'.format(ex))
            return self.file_dict

        print('\nCompleted\n{}Process summary\n{}\nTime: {}\nConnection erorr count: {}\n# of directories: {}'.\
              format("="*50, "="*50, time.time() - self.start_time,\
                     self.connection_error_count, \
                     len(self.file_dict)))
        return self.file_dict


if __name__ == '__main__':

    CRAN_URL = args.BASE_URL
    create_ist = recur_url(args.BASE_URL, args.INIT_PATH)
    result = create_ist.get_result()
    CRAN_STAGE_PATH = '/fsrepo/stage/cran'
    download_total_size, download_total_files = 0,0

    unit_dict = {'': 1, 'K': 1024, 'M': 1024*1024}
    out_unit_dict = {'gb': 1024*1024*1024, 'mb':1024*1024, 'kb':1024, '': 1}

    with open(args.output, 'w') as f:
        json.dump(result, f)

    #print('{}\nCollected data summary\n{}\nSaved meta file: {}\nTotal size: {}({})\nTotal N files: {} '.\
    #      format("="*50, "="*50, args.output, \
    #             round(create_ist.total_size / create_ist.out_unit_dict[args.out_unit],4), args.out_unit, create_ist.total_N_files))

    with open('download_cran.sh','w') as script_file:
        script_file.write('#!/bin/bash\n')

        for package in result['/src/contrib/']:
            lib_name  = result['/src/contrib/'][package]['name']
            lib_path  = result['/src/contrib/'][package]['path']
            file_size = result['/src/contrib/'][package]['size']

            if os.path.exists('%s%s/%s'%(CRAN_STAGE_PATH,lib_path,lib_name)):
                continue
                #stage_file_size = os.stat('%s/%s/%s'%(CRAN_STAGE_PATH, lib_path, lib_name)

            else:
                resize = float(''.join(re.findall(r'\d+|\.',file_size))) * unit_dict[re.findall('[A-Z]', file_size.upper())[0]]
                download_total_size += resize
                download_total_files += 1

                print("%s%s/%s doesn't exists "%(CRAN_STAGE_PATH,lib_path,lib_name))
                script_file.write("wget --connect-timeout=2 --tries=3 -N -P /fsrepo/stage/cran/src/contrib %s%s/%s \n"%(CRAN_URL, lib_path, lib_name))
     
        print('{}\nCollected Meta summary\n{}\nSaved meta file: {}\nTotal size: {}({})\nTotal N files: {} '.\
            format("="*50, "="*50, args.output, \
            round(create_ist.total_size / create_ist.out_unit_dict[args.out_unit],4), args.out_unit, create_ist.total_N_files))

     
        print('{}\nTo Be Download\n{}\nTotal N files : {}\nTotal size:{} ({})'.\
            format("="*50, "="*50, download_total_files, round(download_total_size / out_unit_dict[args.out_unit],4), args.out_unit))

