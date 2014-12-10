#!/usr/bin/env python
import os,sys
import time
import socket
import fcntl
import struct
import pexpect

#UPD

########SSH logon stuff############
default_passwd = "rootroot"
prompt_firstlogin = "Are you sure you want to continue connecting \(yes/no\)\?"
prompt_passwd = "root@.*'s password:"
prompt_logined = "\[root@.*\]#"
prompt_percentage = ".*100%.*"

def Standard_Reply(ssh,IP):
    try:
        #ssh = pexpect.spawn('ssh root@%s' % IP)
        result = ssh.expect([prompt_firstlogin, prompt_passwd, prompt_logined, pexpect.TIMEOUT],timeout=10)
        #ssh.logfile = sys.stdout                                            # printout in real time
        ssh.logfile = None

        if result == 0:
          ssh.sendline('yes')
	  try:
	    ssh.expect(prompt_passwd)
	    ssh.sendline(default_passwd)
	    ssh.expect(prompt_logined)
	  except:
	    print 'no authentication but need record the host info!'
        elif result == 1:
          ssh.sendline(default_passwd)
          ssh.expect(prompt_logined)
        elif result == 2:
          pass
        elif result == 3:
          print "ssh to %s timeout" %IP
          sys.exit(0)
        return ssh,result
    except:
 	result = 'crash'
        print 'Mismatch BTW default expect or unexpected things happen!!'
        return ssh,result
        sys.exit(0)

def Standard_Reply_SCP(ssh,IP):
    try:
        #ssh = pexpect.spawn('ssh root@%s' % IP)
        result = ssh.expect([prompt_firstlogin, prompt_passwd, prompt_logined, pexpect.TIMEOUT, prompt_percentage],timeout=10)
        #ssh.logfile = sys.stdout                                            # printout in real time
        ssh.logfile = None

        if result == 0:
          ssh.sendline('yes')
          ssh.expect(prompt_passwd)
          ssh.sendline(default_passwd)
          ssh.expect(prompt_percentage)
        elif result == 1:
          ssh.sendline(default_passwd)
          ssh.expect(prompt_percentage)
        elif result == 2:
          pass
        elif result == 3:
          print "ssh to %s timeout" %IP
          sys.exit(0)
	elif result == 4:
          pass
        return ssh,result
    except:
 	print "result is ",result
        print 'Mismatch BTW default expect or unexpected things happen!'
        return ssh,result
        #sys.exit(0)

def Standard_Reply_Windows_SCP(ssh,IP):
    try:
        #ssh = pexpect.spawn('ssh root@%s' % IP)
        result = ssh.expect([prompt_firstlogin, prompt_passwd, prompt_logined, pexpect.TIMEOUT, prompt_percentage],timeout=10)
        #ssh.logfile = sys.stdout                                            # printout in real time
        ssh.logfile = None

        if result == 0:
          ssh.sendline('yes')
          ssh.expect(prompt_passwd)
          ssh.sendline(default_passwd)
          ssh.expect(prompt_percentage)
        elif result == 1:
          ssh.sendline(default_passwd)
          ssh.expect(prompt_percentage)
        elif result == 2:
          pass
        elif result == 3:
          print "ssh to %s timeout" %IP
          sys.exit(0)
	elif result == 4:
          pass
        return ssh,result
    except:
 	print "result is ",result
        print 'Mismatch BTW default expect or unexpected things happen!'
        return ssh,result
        #sys.exit(0)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def execute(file,folder):
    date = time.strftime("%Y%m%d", time.localtime())
    T_time = time.strftime("%H:%M:%S", time.localtime())

    #localPWD = os.getcwd()
    #dir = "%s/%s/" % (localPWD,date)
    #subdir = "%s%s/" % (dir,T_time)
    #
    #if os.path.exists(dir) != True:
    #    os.mkdir(dir)
    #
    #os.mkdir(subdir)


    ########command assistant stuff####
    #logfn = "/arroyo/log/serverinfo.log.%s" % date;
    #localfn = "%s/object.local" % subdir
    #dbfn = "/home/isa/bss/database/ctnobj.lst"
    #localdb = "%s/db.local" % subdir
    windows_tag = 0
    try:
        LocalIP = get_ip_address('eth0')
    except:

        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        LocalIP = s.getsockname()[0]
        windows_tag=1

    print 'local IP is ',LocalIP
    ###################################

    #cmd1 = 'rm -rf %s' % logfn
    #cmd2 = 'echo 1 > /proc/calypso/test/reopen_logfiles'
    #cmd3 = 'echo 2 > /proc/calypso/tunables/cm_logserverinfo'
    #cmd4 = 'su - isa -c "cd bss/database/; ./dumpctn > /dev/null"'
    cmd1 = "ssh-keygen -t rsa"
    cmd2 = "chmod 755 ~/.ssh"
    cmd3 = "scp ~/.ssh/id_rsa.pub %s:%s" % (LocalIP,dir)
    cmd4 = "3 return"

    #time.sleep(10)

    f = open(file,'r')
    IP_list = f.readlines()
    f.close()

    os.chdir(folder)
    #os.popen(cmd1)
    #os.popen(cmd2)
    #os.popen(cmd3)
    #os.popen(cmd4)

    ######other nodes handling begin#######
    for x in IP_list:
	x = x.strip()
	x = x.split(':')[-1]
	if x != '':
	    print 'IP is ',x
	#    if x == LocalIP:
	#	os.popen('rm -rf /root/.ssh/id*')
	#	os.popen('ssh-keygen -t rsa')
	#    else:
	    try:
		ssh = pexpect.spawn('ssh root@%s' % x)
		ssh,result = Standard_Reply(ssh,x)
	    except:
		print "ssh to %s error: " % x + ssh.before[:-1]
		print 'result is ',result
		sys.exit(1)

	    ssh.sendline('rm -rf /root/.ssh/id*')
	    ssh.expect(prompt_logined)
	    ssh.sendline('ssh-keygen -t rsa')
	    while True:
		ssh.sendline('')
		try:
		    ssh.expect(prompt_logined,timeout=10)
		except:
		    continue
		break

	    ssh.sendline('chmod 755 ~/.ssh')
	    ssh.expect(prompt_logined)
	    ssh.close()

	    if windows_tag == 1:
		print 'windows IP handled specially'
		try:
		    scp = pexpect.spawn('scp root@%s:/root/.ssh/id_rsa.pub id_rsa.pub_%s' % (x,x))
		    scp,result = Standard_Reply_Windows_SCP(scp,x)
		    #scp.expect('pass*',timeout=2)
		    #scp.sendline('rootroot')
		    #time.sleep(1)
		except:
		    print "scp to %s error: " % x + scp.before[:-1]
		    sys.exit(1)
	    else:
		try:
		    scp = pexpect.spawn('scp root@%s:/root/.ssh/id_rsa.pub id_rsa.pub_%s' % (x,x))
		    scp,result = Standard_Reply_SCP(scp,x)
		    #scp.expect('pass*',timeout=2)
		    #scp.sendline('rootroot')
		    #time.sleep(1)
		except:
		    print "scp to %s error: " % x + scp.before[:-1]
		    sys.exit(1)
    sys.exit(1)




def usage():
    print "usage: " + "[SYNTAX:] python " + "ssh_Xchange.py " + "CFGfile"
    sys.exit(1)


if __name__ == '__main__':
    numargs = len(sys.argv) - 1
    if numargs == 0:
        usage()

    else:
        tag = 0
        action = ''


        file = sys.argv[1]
	folder = sys.argv[2]
	print "INFO:SSH KEY Fetching ongoing......."
        execute(file,folder)

    sys.exit(1)
