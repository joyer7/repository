import sys
import os
import subprocess

if __name__ == '__main__':
    os_type = sys.argv[1]
    print(os_type)
        with open('./conda-forge/%s/repodata.json'%os_type,'r') as read_file:
            with open('download_%s.sh'%os_type,'w') as script_file:
                script_file.write('#!/bin/bash\n')
                data = json.load(read_file)

                for package in data['packages']:
                    package_size = int(data['packages'][package]['size'])
                    package_md5 = data['packages'][package]['md5']

                    if os.path.exists('./conda-forge/%s/%s'%(os_type,package)):
                        real_size = os.stat('./conda-forge/%s/%s'%(os_type,package)).st_size

                            if package_size == real_size:
                                real_md5 = os.popen('md5sum ./conda-forge/%s/%s'%(os_type,package)).read().split(' ')[0]

                                    if package_md5 == real_md5:
                                        print('%s [OK]'%package)
                                    else:
                                        print('%s [BAD] because of md5 checksum failure'%(package))
                                        script_file.write('wget --connect-timeout=2 --tries=3  https://conda.anaconda.org/conda-forge/%s/%s\n'%(os_type,package))
                            else:
                                print('%s [BAD] as The size of %s seems not ok (%d/%d)'%(package,package,real_size,package_size))
                                script_file.write('wget --connect-timeout=2 --tries=3  https://conda.anaconda.org/conda-forge/%s/%s\n'%(os_type,package))
                    else:
                        print("%s [BAD] as %s doesn't exists"%(package,package))
                        script_file.write('wget --connect-timeout=2 --tries=3  https://conda.anaconda.org/conda-forge/%s/%s\n'%(os_type,package))
