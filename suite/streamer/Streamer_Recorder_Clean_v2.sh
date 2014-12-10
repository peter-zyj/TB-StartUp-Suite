#!/bin/bash
echo -n " record fetch Start!"
echo


./AVSDBUtil << EOF > all-content_record
7
2
0
EOF

awk -F "=" '{if($1~/.*Name.*/){print$2}}' all-content_record > simple_records
echo -n " record fetch END!"
echo
num=`wc -l simple_records`
echo -n "the total number of records is $num"
echo
echo -n "Do you want to continue the remove all of these records?  Yes | No ? "

read action

#if [[ $action =~ "(?i).*Y.*" ]];then
if [[ $action =~ .*Y.* || $action =~ .*y.* ]];then
chmod 777 simple_records
sleep 2

echo -n " record remove Start!"
echo

if [ -s simple_records ];then
action="None"
LoopCalc=0

for record in $(cat simple_records)
do
actionTag="false"
action=$action"\n7\n1\n$record"
LoopCalc=$((LoopCalc+1))
if [[ "$LoopCalc" == "300" ]];then
    action=$action"\n0\n"
    #echo "action is $action"
    actionTag="true"
    #exit
        
./AVSDBUtil << EOF
$action
EOF

fi

done

if [[ "$actionTag" != "true" ]];then
action=$action"\n0\n"
#echo "action is $action"
./AVSDBUtil << EOF
$action
EOF

fi

fi
echo
echo -n " record remove End!"
echo
fi
echo -n "Bye!"
echo
