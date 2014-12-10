rm -rf ~/dump_loop 2>/dev/null
mkdir ~/dump_loop
cd ~/dump_loop
  
D=`date  +%Y%m%d`
rm -rf /arroyo/log/serverinfo.log.$D
echo 1 > /proc/calypso/test/reopen_logfiles
echo 2 > /proc/calypso/tunables/cm_logserverinfo
su - isa -c "cd bss/database/; ./dumpctn > /dev/null"

sleep 5
cp /arroyo/log/serverinfo.log.$D ~/dump_loop/object.local
cp /home/isa/bss/database/ctnobj.lst  ~/dump_loop/db.local
~/avs_clist ~/dump_loop/db.local verbose ~/dump_loop/object.local > ~/dump_loop/verbose.local

awk '/.*orphaned.*/' ~/dump_loop/verbose.local

