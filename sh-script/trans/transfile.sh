set -e

S_FILE="$1"  # Source File
T_FILE="$2" # Target File
T_HOST="$3" # Target Host
T_OWNER="$4" # Target Owner
T_PERM="$5" # Target Permission
JAVA_HOME="$6" # JAVA HOME

# Return Code
EXIT_SUCC=0
EXIT_FAIL=1

unalias -a
PATH=$JAVA_HOME/bin:$PATH:.
export PATH
HOST_NAME=`hostname`
#WHOAMI=`whoami`

# --------------------------------------------------------------- #
# Main
# --------------------------------------------------------------- #

printf "@ -------------------------------------------------------------#\n"
#printf "@ ==> (TASK)  HostName(${HOST_NAME}), Run_User(${WHOAMI})\n"
printf "@ ==> (TASK)  HostName(${HOST_NAME}) \n"
printf "@ -------------------------------------------------------------#\n"
                
#KM_HOME=$( cd $(dirname `ls -l $0 | awk '{ print $NF }'`) && pwd )
KM_HOME=/unify/ezra/ezra_ag_dev/km
echo "@ ==> (INFO)  KM_HOME = ${KM_HOME}"

if [ ! -d "${KM_HOME}/../plugin" ]
then
echo "@ ==> (ERROR) /KM_HOME/../plugin: No such directory"
exit 2
fi

cd ${KM_HOME}/../plugin  

for i in ./*.jar; do
   CLASSPATH=$CLASSPATH:$i
done
export CLASSPATH

java -cp $CLASSPATH plugin.FileTrans FT "${S_FILE}" "${T_FILE}" ${T_HOST} ${T_OWNER} ${T_PERM} 2>&1

########################  End of script  ########################
