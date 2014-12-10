#!/bin/bash

if [[ $@ == "" ]];then
    echo -n "EG: ./BatchInsall.sh CFG_file [-ssh|-all|-streamer|-vault|-cdsm|-cache|-recorder] "
    echo
    exit
fi


echo -n "Start from Scratch now......."
echo



if [[ $2 == "-ssh" ]];then
    mkdir temp_folder
    echo -n "#######SSH Authentication clearing ......."
    echo
    ./ssh_Xchange.py $1 temp_folder
    cd temp_folder
    cat id_* > authorized_keys
    
    cd ..
    ./dataTransfer.py temp_folder/authorized_keys /root/.ssh $1 all
    echo -n "#######SSH Authentication Done!!"
    echo
    rm -rf temp_folder
fi



if [[ $2 == "-vault" || $3 == "-vault" ]];then
    echo -n "#######VAULT software transfer ongoing......."
    echo
    tar -cvf vault.tar vault
    ./dataTransfer.py vault/listcontent /arroyo/db $1 vault
    ./dataTransfer.py vault.tar /root $1 vault
    echo -n "#######VAULT software transfer Done!!"
    echo
fi

if [[ $2 == "-streamer" || $3 == "-streamer" ]];then
    echo -n "#######STREAMER software transfer ongoing......."
    echo
    tar -cvf streamer.tar streamer
    ./dataTransfer.py streamer/listsession /arroyo/db $1 streamer
    ./dataTransfer.py streamer/Streamer_Recorder_Clean.sh /arroyo/db $1 streamer
    ./dataTransfer.py streamer.tar /root $1 streamer
    echo -n "#######STREAMER software transfer Done!!"
    echo
fi

if [[ $2 == "-cdsm" || $3 == "-cdsm" ]];then
    echo -n "#######CDSM software transfer ongoing......."
    echo
    tar -cvf cdsm.tar cdsm

    ./dataTransfer.py cdsm.tar /root $1 cdsm
    echo -n "#######CDSM software transfer Done!!"
    echo
fi


if [[ $2 == "-cache" || $3 == "-cache" ]];then
    echo -n "#######cache software transfer ongoing......."
    echo
    tar -cvf cache.tar cache

    ./dataTransfer.py cache.tar /root $1 cache
    echo -n "#######cache software transfer Done!!"
    echo
fi

if [[ $2 == "-vvim" || $3 == "-vvim" ]];then
    echo -n "#######vvim software transfer ongoing......."
    echo
    tar -cvf vvim.tar vvim

    ./dataTransfer.py vvim.tar /root $1 vvim
    echo -n "#######vvim software transfer Done!!"
    echo
fi

if [[ $2 == "-recorder" || $3 == "-recorder" ]];then
    echo -n "#######recorder software transfer ongoing......."
    echo
    tar -cvf recorder.tar recorder

    ./dataTransfer.py recorder.tar /root $1 recorder
    echo -n "#######recorder software transfer Done!!"
    echo
fi

if [[ $2 == "-all" || $3 == "-all" ]];then
    echo -n "#######all software transfer ongoing......."
    echo
    tar -cvf cdsm.tar cdsm
    tar -cvf streamer.tar streamer
    tar -cvf vault.tar vault
    tar -cvf vvim.tar vvim
    tar -cvf cache.tar cache
    tar -cvf recorder.tar recorder
    ./dataTransfer.py cdsm.tar /root $1 cdsm
    ./dataTransfer.py streamer.tar /root $1 streamer
    ./dataTransfer.py vault.tar /root $1 vault
    ./dataTransfer.py vvim.tar /root $1 vvim
    ./dataTransfer.py cache.tar /root $1 cache
    ./dataTransfer.py recorder.tar /root $1 recorder
    echo -n "#######all software transfer Done!!"
    echo
fi

echo -n "&&&&&&&&&&&&&&&&&COMMON PART&&&&&&&&&&&&&&&&&&&&"
echo
echo -n "Action:Do U want to Common install the tool backgroud(eg: pexpect) Yes|No?"

read action

#if [[ $action =~ "(?i).*Y.*" ]];then
if [[ $action =~ .*Y.* || $action =~ .*y.* ]];then
    ./Common_Module_install.py $1
fi
echo -n "&&&&&&&&&&&&&&&&&&FINISHED&&&&&&&&&&&&&&&&&&&&&"
echo
