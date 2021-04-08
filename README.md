
# Repository 
Local Repository 
- Kolon Benit, BigData Analytics Team, Austin Rho, (Shin Seok)
- last update: 2020.03.01 

## 0. Architecture
- DMZ : External Library Server
- Local : Local Library Server
- Process : 
**External Library Server**
  1. Download Libraries in an External Server
  2. Compress & Transport libraries to Local Library Server
**Local Library Server**
  1. Uncompress libraries files
  2. Copy files to Local Library Path


## A. Code List

**1. Making Local Repository**

    - 00.manage.sh : Execute all sh-files 01~08xxxxx.sh
    - 01.make-meta.sh : Create the latest R, Conda, and Conda-Forge meta files
    - 02.make-download-copy-script.sh : Compare files with local library files & make download scripts 
    - 03.download-repo.sh : download libraries from cran, conda, conda-forge
	- 04.copy-repo.sh : Copy downloaded new file to local repository
	- 05.compress-split.sh 
	- 06.trans_file.sh : transport files to Local Library Server
	- 07.delete-file : Delete downloaded file which is new
	- 08.check-current-reposist.sh : Checking

**2. ./py-script/**

    - make-cran-meta.py : Create R meta file 
    - make-current-repo.py : Compare libraries
	- make-download-copy-script.py : Make download script

**3. ./sh-script/**

    - ./compress/
	- ./delete/
	- ./py-script/verify-current-repo.py
	- ./trans/
	- ./uncompress/
    - copy*.sh
	- download*.sh
	- dportal-copy.*

## B. R U Ready?
    - windows key + R
    - type "CMD"  and run CMD Window
    - type "git clone https://github.com/joyer7/repository.git" on command window
    - Enjoy It !!!
    

## C. Question & Answer
Please feel free to contact Austin Rho 
    - ssrho@kolon.com, injoyer@yonsei.ac.kr


