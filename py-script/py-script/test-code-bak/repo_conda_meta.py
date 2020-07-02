import sys
import os
import json
import subprocess

if __name__ == '__main__':
    
    repo_type = sys.argv[1]
    os_type = sys.argv[2]

    if repo_type == "conda":
        url = 'https://repo.anaconda.com/pkgs/main'
        path = '/fsrepo/stage/conda/repo.continuum.io/pkgs/main'
        
    else:
        url ='https://conda.ananconda.org/conda-forge'
        path = '/fsrepo/stage/conda-forge/conda.anaconda.org/conda-forge'

    print(os_type)
    with open('%s/%s/repodata.json'%(path,os_type),'r') as read_file:
        with open('download_%s_%s.sh'%(repo_type,os_type),'w') as script_file:
            script_file.write('#!/bin/bash\n')
            data = json.load(read_file)

            print(type(data))

            for package in data['packages']:
            
                package_size = int(data['packages'][package]['size'])
                package_md5 = data['packages'][package]['md5']

                # File Exists Check 
                if os.path.exists('%s/%s/%s'%(path,os_type,package)):
                    real_size = os.stat('%s/%s/%s'%(path,os_type,package)).st_size
                    
                    # File Size Check
                    if package_size == real_size:
                        real_md5 = os.popen('md5sum %s/%s/%s'%(path,os_type,package)).read().split(' ')[0]
                        
                        # File Checksum Check
                        if package_md5 == real_md5: 
                            print('%s [OK]'%package)
                        else:
                            print('%s [BAD] because of md5 checksum failure'%(package))
                            script_file.write('wget --connect-timeout=2 --tries=3 %s/%s/%s\n'%(url,os_type,package))
                    else:
                        print('%s [BAD] as The size of %s seems not ok (%d/%d)'%(package,package,real_size,package_size))
                        script_file.write('wget --connect-timeout=2 --tries=3 %s/%s/%s\n'%(url,os_type,package))
                else:
                    print("%s [BAD] as %s doesn't exists"%(package,package))
                    script_file.write('wget --connect-timeout=2 --tries=3  %s/%s/%s\n'%(url, os_type,package))
