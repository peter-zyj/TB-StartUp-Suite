#!/usr/local/bin/python
#encoding=utf-8
#filename=check_multicast.py

# UDP multicast examples, Hugo Vincent, 2005-05-14.
import socket
import fcntl 
import struct 
import sys,os
import traceback
import time
import signal

if not hasattr(socket, 'IP_ADD_SOURCE_MEMBERSHIP'):
    setattr(socket, 'IP_ADD_SOURCE_MEMBERSHIP', 39)



def handler(signum, frame):
    print 'Timeout'

signal.signal(signal.SIGALRM, handler)


def time_up():
    print "keep old version of IGMP!"

def raw_input_with_timeout(x):    
    answer = 'n'
    signal.alarm(x)
    try:
    	answer = raw_input("")
    except:
	   print "keep old version of IGMP!"
    signal.alarm(0)
    return answer

def get_ip_address(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl( 
        s.fileno(), 
        0x8915,  # SIOCGIFADDR 
        struct.pack('256s', ifname[:15]) 
    )[20:24]) 
 

def send(data, port=50000, addr='239.192.1.100'):
        """send(data[, port[, addr]]) - multicasts a UDP datagram."""
        # Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Make the socket multicast-aware, and set TTL.
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
        # Send the data
        s.sendto(data, (addr, port))

def recv3(port, addr, localip, buf_size=1024):
        """recv([port[, addr[,buf_size]]]) - waits for a datagram and returns the data."""
        
        # Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set some options to make it multicast-friendly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
                pass # Some systems don't support SO_REUSEPORT
        s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
        s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
        
        # Bind to the port
        s.bind(('', port))
        
        # Set some more multicast options
        #intf = socket.gethostbyname(socket.gethostname())
	add2 = '192.169.210.1'
	#print 'add2 is::==',add2
        s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(localip))
        #s.setsockopt(socket.SOL_IP, socket.IP_ADD_SOURCE_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(add2) + socket.inet_aton(localip))
        if version == 3:
            zyj = (socket.inet_aton(addr) +
                   socket.inet_aton(localip) +
                   socket.inet_aton(add2))
            s.setsockopt(socket.SOL_IP, socket.IP_ADD_SOURCE_MEMBERSHIP, zyj)
        else:
            zyj = (socket.inet_aton(addr) +
                   socket.inet_aton(localip))

            s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, zyj)

       
        s.settimeout(1) 
        # Receive the data, then unregister multicast receive membership, then close the port
        data = ""
        try:
            data, sender_addr = s.recvfrom(buf_size)
        except socket.timeout, e:
            raise socket.timeout, e
        #s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
        s.close()
        return data




ip = "239.1.2.3"
port = 10001
interface = "eth1"
if __name__ == '__main__':
  help = "Check whether the multicast packets' receiving is OK at specified interface and multicast ip and address.\n\
Usage: %s ip port interface, or\n\
       %s ip port(interface is 'eth1' by default), or\n\
       %s (default as %s %s %s eth1)\n\
Example: %s 239.1.2.3 10002 eth1" %(__file__, __file__, __file__, __file__, ip, str(port), __file__)
  try:
    if len(sys.argv) == 2 and (sys.argv[1]=="--help" or sys.argv[1]=='-h'):
       print help
       sys.exit()
    
    if len(sys.argv) >= 2:
      port = int(sys.argv[2])
      ip = sys.argv[1]
    if len(sys.argv) == 4:
      interface = sys.argv[3]

    localip = get_ip_address(interface)
    print "%s's ip address is: %s" %(interface, localip)
 
    version = 3 #default IGMP version
    for i in range(10):
        try:
            a = recv3(port, ip, localip, version)
        except socket.timeout:
            print "Maybe IGMPv2 are the under running,PRESS [Y] for V2, otherwise,Waiting data at %s from %s port %s timeout!" %(localip, ip, port)
            answer = raw_input_with_timeout(2)
	    if answer == "Y" or answer == "y":
	           version = 2
	           for y in range(10):
      	           	try:
       		           a = recv3(port, ip, localip, version)
                    	except socket.timeout:
         	           print "Waiting data at %s from %s port %s timeout!" %(localip, ip, port)
                           continue
                    	if len(a):
                           print "IGMPV2::Recv data at %s from %s port %s successful!" %(localip, ip, port)
	           break
            continue
        if len(a):
            print "IGMPV3::Recv data at %s from %s port %s successful!" %(localip, ip, port)

  except:
    traceback.print_exc()
    print help
