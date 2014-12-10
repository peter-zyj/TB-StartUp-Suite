#!/bin/sh
echo -n "Kill all the streamer session incluing the abnormal sessionHandler!"
echo
echo -n "session fetch started!"
echo

./AVSDBUtil << EOF > all-sessionHandler
6
2
0
EOF

awk -F "=" '/.*SessionHandle.*/{gsub(/^[ \t]+/,"",$2);gsub(/$[ \t]+/,"",$2);print $2}' all-sessionHandler > simple_sessionHandler
#awk -F "=" '{if($1~/.*Name.*/){print$2}}' all-sessionHandler > simple_sessionHandler
echo -n " session fetch END!"
echo
num=`wc -l simple_sessionHandler`
echo -n "the total number of sessions is $num"
echo
echo -n "Do you want to continue the remove all of these sessions?  Yes | No ? "

read action

#if [[ $action =~ "(?i).*Y.*" ]];then
if [[ $action =~ .*Y.* || $action =~ .*y.* ]];then
chmod 777 simple_sessionHandler
sleep 2

echo -n " session remove Start!"
echo

if [ -s simple_sessionHandler ];then
for record in $(cat simple_sessionHandler)
do
./AVSDBUtil << EOF
6
1
$record
0
EOF
done
fi
echo
echo -n " session remove End!"
echo
fi
echo -n "Bye!"
echo

