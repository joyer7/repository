# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:50:57 2020
@author: hyeongyuy

command example:
    python3 cp_conda_forge.py --source /fsrepo/stage/conda-forge/conda.anaconda.org/conda-forge/linux-64 --dest /fsrepo/conda-forge/conda.anaconda.org/conda-forge/linux-64 --outname cp_conda_forge_linux64.sh

"""
import argparse
import os

#set args
parser = argparse.ArgumentParser('')
parser.add_argument('--type', dest ='type', default = 'conda')
#parser.add_argument('--source', dest ='source', default = '/fsrepo/stage/conda-forge/conda.anaconda.org/conda-forge')
#parser.add_argument('--dest', dest ='dest', default = '/fsrepo/conda-forge/conda.anaconda.org/conda-forge')
#parser.add_argument('--outname', dest ='outname', default = 'cp_conda_forge.sh')
args = parser.parse_args()
print(args)

source = ""
dest = ""
outName = ""

if 








cmd_line = ''
for dirname, dirnames, filenames in os.walk(args.source):
    for dir_ in dirnames:
        srcdir = os.path.join(dirname, dir_)
        destdir = srcdir.replace(args.source, args.dest)

        if not os.path.exists(destdir):
            os.makedirs(destdir)
            
    for file_ in filenames:
        srcfile = os.path.join(dirname, file_)
        destfile = srcfile.replace(args.source, args.dest)
        
        srcfile_size = os.stat(srcfile).st_size
        
        if os.path.exists(destfile):
            dest_size = os.stat(destfile).st_size
          
            # File Size Check
            if srcfile_size == dest_size:
                src_md5 = os.popen('md5sum {}'.format(srcfile)).read().split(' ')[0]
                dest_md5 = os.popen('md5sum {}'.format(destfile)).read().split(' ')[0]

                # File Checksum Check
                if src_md5 == dest_md5:
                    print('[OK] %s'%srcfile)
                else:
                    print('[BAD] %s because of md5 checksum failure'%(srcfile))
                    cmd_line += 'echo \"copied {}\"\n'.format(srcfile)
                    cmd_line += 'cp {} {}\n'.format(srcfile, destfile)
            else:
                print('[BAD] The size of %s seems not ok (%d/%d)'%(srcfile, dest_size,srcfile_size))
                cmd_line += 'echo \"copied {}\"\n'.format(srcfile)
                cmd_line += 'cp {} {}\n'.format(srcfile, destfile)
                
        else:
            print("[BAD] %s doesn't exists"%(srcfile))
            cmd_line += 'echo \"copied {}\"\n'.format(srcfile)
            cmd_line += 'cp {} {}\n'.format(srcfile, destfile)

      
      
with open(args.outname, 'w') as s:
    s.write(cmd_line)

  
