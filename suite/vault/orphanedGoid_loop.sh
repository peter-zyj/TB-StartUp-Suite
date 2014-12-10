#!/bin/bash

#if [[ $@ == "" ]];then
#    echo -n "EG: ./orphanedGoid.sh"
#    echo
#    exit
#fi

#add the follwing sentence in .bash_profile before the script
#ps -ef | grep orphanedGoid_loop | grep -v grep | awk '{print $2}'|xargs kill -9 2>/dev/null
#pgrep orphanedGoid_loop | xargs kill -9
rm -rf ~/dump_loop 2>/dev/null
mkdir ~/dump_loop
cd ~/dump_loop
echo > previous_orphanedGoid.log
tag=True
while true
do
    D=`date  +%Y%m%d`
    rm -rf /arroyo/log/serverinfo.log.$D
    echo 1 > /proc/calypso/test/reopen_logfiles
    echo 2 > /proc/calypso/tunables/cm_logserverinfo
    su - isa -c "cd bss/database/; ./dumpctn > /dev/null"
    
    sleep 5
    cp /arroyo/log/serverinfo.log.$D ~/dump_loop/object.local
    cp /home/isa/bss/database/ctnobj.lst  ~/dump_loop/db.local
    ~/avs_clist ~/dump_loop/db.local verbose=2 ~/dump_loop/object.local > ~/dump_loop/verbose.local
    
    awk '/.*orphaned.*/' ~/dump_loop/verbose.local > current_orphanedGoid.log
    #echo "*************************!Attention!********************************"
    sleep 5
    if [[ $tag == "True" ]];then
        awk 'ARGIND==1{a[$0]}ARGIND>1&&!($0 in a){print "";print "***********Attention*********";print $0}' previous_orphanedGoid.log current_orphanedGoid.log
        cp ~/dump_loop/current_orphanedGoid.log ~/dump_loop/previous_orphanedGoid.log
    else
        awk 'ARGIND==1{a[$0]}ARGIND>1&&!($0 in a){print "";print "***********Attention*********";print $0}' previous_orphanedGoid.log current_orphanedGoid.log | tee -a previous_orphanedGoid.log
        #echo "********************************************************************"
        #cp ~/dump_loop/current_orphanedGoid.log ~/dump_loop/previous_orphanedGoid.log
    fi
    sleep 5
    tag=False
done


