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
        result = ssh.expect([prompt_firstlogin, prompt_passwd, prompt_logined, pexpect.TIMEOUT],timeout=2)
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
        result = ssh.expect([prompt_firstlogin, prompt_passwd, prompt_logined, pexpect.TIMEOUT, prompt_percentage],timeout=2)
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
        result = ssh.expect([prompt_firstlogin, prompt_passwd, prompt_logined, pexpect.TIMEOUT, prompt_percentage],timeout=2)
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

def execute(file):    
    date = time.strftime("%Y%m%d", time.localtime())
    T_time = time.strftime("%H:%M:%S", time.localtime())

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


    cmd1 = 'tar -xvf pexpect-2.3.tar'
    cmd2 = 'cd pexpect-2.3'
    cmd3 = 'python setup.py install'
    #time.sleep(10)
    
    f1 = open(file,'r')
    IP_list = f1.readlines()
    f1.close()

    cmd4 = './dataTransfer.py common/pexpect-2.3.tar /root %s all' % (file)
    os.system(cmd4)
    
    cmd5 = './dataTransfer.py common/coredump.sh /root %s all' % (file)
    os.system(cmd5)
    
    cmd6 = './dataTransfer.py common/lrzsz-0.12.20-22.1.x86_64.rpm /root %s all' % (file)
    os.system(cmd6)
    
    cmd7 = './dataTransfer.py common/orphanedGoid.sh /root %s all' % (file)
    os.system(cmd7)
    ######other nodes handling begin#######
    for x in IP_list:
	x = x.strip()
	x = x.split(':')[-1]
	if x != '':
	    print 'IP is ',x

	    try:
		ssh = pexpect.spawn('ssh root@%s' % x)
		ssh,result = Standard_Reply(ssh,x)
	    except:
		print "ssh to %s error: " % x + ssh.before[:-1]
		print 'result is ',result
		sys.exit(1)
	    
	    ssh.sendline('cd /root')
	    ssh.expect(prompt_logined) 

	    ssh.sendline(cmd1)
	    ssh.expect(prompt_logined)
	   
	    ssh.sendline('chmod 777 pexpect-2.3')
	    ssh.expect(prompt_logined)

	    ssh.sendline(cmd2)
	    ssh.expect(prompt_logined)

	    ssh.sendline(cmd3)
	    ssh.expect(prompt_logined)

	    ssh.sendline('cd /root')
	    ssh.expect(prompt_logined)
	        
	    ssh.sendline('rpm -ivh lrzsz-0.12.20-22.1.x86_64.rpm')
	    ssh.expect(prompt_logined)
	    
	    ssh.sendline('rm -rf pexpect-2.3*')
	    ssh.expect(prompt_logined)

	    ssh.sendline('rm -rf lrzsz-0.12.20-22.1.x86_64.rpm')
	    ssh.expect(prompt_logined)

	    ssh.sendline("(grep 'coredump.sh -p' .bash_profile) || (echo './coredump.sh -p' >> .bash_profile)")
	    ssh.expect(prompt_logined)

	    ssh.sendline("(grep './coredump.sh -loop &' .bash_profile) || (echo './coredump.sh -loop &' >> .bash_profile)")
	    ssh.expect(prompt_logined)
	
	    #ssh.sendline("(grep 'pgrep orphanedGoid_loop | kill -9' .bash_profile) || (echo 'pgrep orphanedGoid_loop | kill -9' >> .bash_profile)")
	    #ssh.expect(prompt_logined)
	    #
	    #ssh.sendline("(grep './orphanedGoid_loop.sh &' .bash_profile) || (echo './orphanedGoid_loop.sh &' >> .bash_profile)")
	    #ssh.expect(prompt_logined)

	    ssh.close()
    sys.exit(1)

    
   
    
def usage():
    print "usage: " + "[SYNTAX:] python " + "Common_Module_install.py " + "CFGfile"         
    sys.exit(1)


if __name__ == '__main__':
    numargs = len(sys.argv) - 1
    if numargs == 0:
        usage()
     
    else:
        tag = 0
        action = ''
        
   
        file = sys.argv[1]
	#folder = sys.argv[2]
	print "INFO:Module and Startup Script Installing ongoing......."
        execute(file)
    
    sys.exit(1) 
