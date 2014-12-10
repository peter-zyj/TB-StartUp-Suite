sw2
interface range fastethernet 0/8 , fastethernet 0/13
switchport mode access
switchport access vlan 5
spanning-tree portfast

interface range fastethernet 0/9 , fastethernet 0/14
switchport mode access
switchport access vlan 100
spanning-tree portfast

interface range fastethernet 0/11 , fastethernet 0/15
switchport mode access
switchport access vlan 3
spanning-tree portfast

interface range fastethernet 0/12 , fastethernet 0/16
switchport mode access
switchport access vlan 8
spanning-tree portfast

asa1
hostname asa1

interface ethernet 0/0
nameif outside
security-level 0
ip address 7.7.5.10 255.255.255.0
no shutdown

interface ethernet 0/2
nameif inside
security-level 100
ip address 7.7.3.10 255.255.255.0
no shutdown

interface ethernet 0/3
nameif dmz
security-level 50
ip address 7.7.8.10 255.255.255.0
ospf authentication message-digest
ospf message-digest-key 1 md5 cisco

route inside 0 0 7.7.3.2

router ospf 1
router-id 8.8.8.8
network 7.7.5.0 255.255.255.0 area 0
network 7.7.8.0 255.255.255.0 area 1
area 0 filter-list prefix abc in
area 1 authentication message-digest

prefix abc deny 192.168.11.11/32
prefix abc deny 192.168.22.22/32
prefix abc permit 0.0.0.0/0 le 32


access-list out extended permit icmp any any
access-group out in in outside
access-list dmz extended permit icmp any any
access-group dmz in in outside

~~~~~~~~~~~~~~~~~~~~~~~~~~

asa1:

interface ethernet 0/0
ip address 7.7.5.10 255.255.255.0 standby 7.7.5.11

interface ethernet 0/1
no shutdown

interface ethernet 0/2
ip address 7.7.3.10 255.255.255.0 standby 7.7.3.11

interface ethernet 0/3
ip address 7.7.8.10 255.255.255.0 standby 7.7.8.11

failover lan unit primary
failover lan interface fover ethernet 0/1
failover key cisco
failover link fover ethernet 0/1
failover interface ip fover 7.7.100.100 255.255.255.0 standby 7.7.100.101
failover

asa2:
interface ethernet 0/1
no shutdown

failover lan unit secondary
failover lan interface fover ethernet 0/1
failover key cisco
failover link fover ethernet 0/1
failover interface ip fover 7.7.100.100 255.255.255.0 standby 7.7.100.101
failover


~~~~~~~~~~~~~~~~~~~~~~~~

sw4

interface fastethernet 0/11
switchport mode access
switchport access vlan 3
spanning-tree portfast

interface fastethernet 0/12
switchport access vlan 2
switchport mode access
spanning-tree portfast

interface fastethernet 0/13
switchport mode access
switchport access vlan 4
spanning-tree portfast

asa3

mac-address auto

interface ethernet 0/0
no shutdown
interface ethernet 0/1
no shutdown
interface ethernet 0/2
no shutdown

delete admin.cfg
delete c1.cfg
delete c2.cfg

admin-context admin
context admin
allocate-interface ethernet 0/2
config-url disk0:/admin.cfg


conext c1
allocate-interface ethernet 0/0
allocate-interface ethernet 0/1
config-url disk0:/c1.cfg

context c2
allocate-interface ethernet 0/0
allocate-interface ethernet 0/2
config-url disk0:/c2.cfg

changto context admin
interface ethernet 0/2
nameif management
security-level 100
ip address 7.7.4.200 255.255.255.0


route management 0 0 7.7.4.1
telnet 7.7.4.1 255.255.255.255 management


changto context c1
interface ethernet 0/0
nameif outside
security-level 0
ip address 7.7.3.8 255.255.255.0

interface ethernet 0/1
nameif inside
security-level 100
ip address 7.7.2.10 255.255.255.0

route outside 0 0 7.7.3.2

access-list out extended permit icmp any any
access-group out in in outside


changto context c2

interface ethernet 0/0
nameif outside
security-level 0
ip address 7.7.3.12 255.255.255.0

interface ethernet 0/2
nameif inside
security-level 100
ip address 7.7.4.10 255.255.255.0



route inside 0 0 7.7.4.1
route outside 7.7.0.0 255.255.0.0 7.7.3.2
route outside 192.168.33.33 255.255.255.255 7.7.3.2

access-list out extended permit icmp any any
access-list out extended permit tcp any any
access-list telent extended permit tcp any any
access-group out in in outside


class-map telnet
match access-list telnet

policy-map telnet
class telnet
set connect conn-max 2

service-policy telnet interface outside


object-group network nat1
	network-object 7.7.4.0 255.255.255.0
object-group network nat2
	network-object 10.10.4.0 255.255.255.0
object-group network nat3
	network-object 192.168.0.0 255.255.0.0

nat (inside,outside) source static nat1 nat2 destination static nat3 nat3



sw1:
ip route 192.168.33.33 255.255.255.255 7.7.4.10

sw5
ip route 192.168.33.33 255.255.255.255 7.7.4.10

R3:
router ospf 1
	redistribute connected subnet


~~~~~~~~~~~


sw3:

interface fastethernet 0/13
switchport mode access
switchport access vlan 77
spanning-tree portfast

sw6:
interface fastethernet 0/7
switchport mode access
switchport access vlan 7
spanning-tree portfast

asa4


show firewall
firewall transparent

ip address 7.7.7.10 255.255.255.0

hostname asa4

interface ethernet 0/0
nameif outside
security-level 0
no shutdown


interface ethernet 0/3
nameif inside
security-level 100
no shutdown

route outside 0 0 7.7.7.3
route inside 7.7.9.0 255.255.255.0 7.7.7.2

nat control

access-list out extended permit icmp any any
access-group out in in outside

access-list nat extended permit ip 7.7.9.0 255.255.255.0 7.7.0.0 255.255.0.0
access-list nonat extended permit ip 7.7.7.0 255.255.255.0 7.7.0.0 255.255.0.0
access-list nonat extended permit ip 7.7.7.0 255.255.255.0 150.1.0.0 255.255.0.0



static (inside,outside)200.200.9.0 access-list nat
nat (inside) 0 access-list nonat

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sw1

interface fastethernet 1/0/12
switchport access vlan 4
switchport mode access
spanning-tree portfast



test-pc:
route add 7.7.0.0 mask 255.255.0.0 150.1.7.254


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sw5:
interface fastethernet 0/1
switchport mode trunk
switchport trunk encapsulation dot1q
no shutdown

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sw1
interface fastethernet 1/0/7
switchport mode access
switchport access vlan 4
spanning-tree
no shutdown



asa3

access-list wsa extended permit ip host 7.7.4.150 any
access-list wccp extended permit tcp any any eq 80
access-list wccp extended permit tcp any any eq 443

wccp 90 redirect-list wccp group-list wsa
wccp interface inside 90 redirect in

R3

ip http server
~~~~~~~~~~~~~~~~
r1
ip http server
ntp server 7.7.4.1

crypto key generate rsa modulus 1024 label ciscoca exportable
crypto key export rsa ciscoca pem url nvram: 3des ciscoca

crypto pki server ciscoca
issuer-name CN=ciscoca.cisco.com L=LA C=US
grant auto
lifetime crl 24
lifetime certificate 200
lifetime ca-sertificate 365
no shutdown

cisco123
cisco123
write

R4
ntp server 7.7.4.1

R5
ntp server 7.7.4.1

asa1
ntp server 7.7.4.1

access-list out extended permit udp any host 7.7.4.1 eq 123
access-list out extended permit tcp any host 7.7.8.1 www
access-list dmz extended permit udp host 7.7.8.1 host 7.7.4.1 eq 123

asa3/c2
access-list out extended permit udp any host 7.7.4.1 eq 123


~~~~~~~~~

aaa new-model
aaa authentication login default line none
aaa authentication login ezvpn local
aaa authorization network ezvpn local

line console 0
login authentication default

username cisco password cisco
ip lcoal pool pool2 13.1.1.1 13.1.1.100

crypto isakmp policy 10
encr 3des
authentication pre-share
group 2

crypto isakmp client configuration group ciscoikev1
key cisco
pool pool2
save-password

crypro isakmp profile ikev1remotes
match identity group ciscoikev1
client authentication list ezvpn
isakmp authorization list ezpvpn
client configuration address respond
virtual-template 2
local-address 7.7.19.3

crypto ipsec transform-set eztrans esp-3des esp-md5-hmac
	mode transparent

crypto ipsec profile ezprof
set transform-set eztrans
set isakmp-profile ikev1remotes

interface virtual-template2 type tunnel
ip unnumbered fastethernet 0/1.2
tunnel source fastethernet 0/1.2
tunnel mode ipsec ipv4
tunnel protection ipsec profile ezprof

R3

ip access-list extended ezvpn-acl permit ip host 7.7.53.3 host 192.168.6.1

crypto ipsec client ezvpn ez
connect acl ezvpn-acl
group ciscoikev1 key cisco
mode client
peer 7.7.19.3
username cisco password cisco

interface f0/1.1
ip address dhcp
crypto ipsec client ezvpn ez

interface loopback 0
ip address 7.7.53.3 255.255.255.255
crypto ipsec client ezpvn ez


ip route 192.168.6.1 255.255.255.255 7.7.19.3

ping 192.168.6.1 source loopback 0



~~~~~~~~~~~~~~~
R1

crypto isakmp policy 10
encr 3des
authentication pre-share
group 2

crypto isakmp key cisco address 0.0.0.0

crypto ipsec transform-set dmtranz esp-3des esp-sh-hmac
	mode transparent

crypto ipsec profile DMVPN
	set transform-set dmtranz

interface tunnel 0
	ip address 172.16.23.1 255.255.255.0
	tunnel source 7.7.8.1
	tunnel key 123
	tunnel mode gre multipoint
	tunnel protection ipsec profile DMVPN
	ip nhrp network-id 123
	ip nhrp authentication cisco
	ip nhrp map multicast dynamic
	ip nhrp redirect
	no ip split-horizon eigrp 123
	ip mtu 1360


router eigrp 123
network 10.0.0.0
network 172.16.0.0
no auto-summary


R2
crypto isakmp policy 10
encr 3des
authentication pre-share
group 2

crypto isakmp key cisco password 0.0.0.0

crypto ipsec transform-set dmtranz esp-3des esp-sh-hmac
	mode transparent

crypto ipsec profile DMVPN
	set transform-set dmtranz

interface tunnel 0
	ip address 172.16.23.2 255.255.255.0
	tunnel source 7.7.8.2
	tunnel key 123
	tunnel mode gre multipoint
	tunnel protection ipsec profile DMVPN
	ip nhrp network-id 123
	ip nhrp authentication cisco
	ip nhrp map multicast dynamic
	ip nhrp redirect
	no ip split-horizon eigrp 123
	ip mtu 1360

router eigrp 123
network 10.0.0.0
network 172.16.0.0
no auto-summary


R4
crypto isakmp policy 10
encr 3des
authentication pre-share
group 2

crypto ipsec transform-set dmtranz esp-3des esp-sh-hmac
	mode transparent

crypto ipsec profile DMVPN
	set transform-set dmtranz

interface tunnel 0
	ip address 172.16.23.4 255.255.255.0
	tunnel source 7.7.6.4
	tunnel key 123
	tunnel mode gre multipoint
	tunnel protection ipsec profile DMVPN
	ip nhrp network-id 123
	ip nhrp authentication cisco
	ip nhrp map  172.16.23.1 7.7.8.1
	ip nhrp map  172.16.23.2 7.7.8.2
	ip nhrp map multicast 7.7.8.1
	ip nhrp map multicast 7.7.8.2
	ip nhrp nhs 172.16.23.1
	ip nhrp nhs 172.16.23.2
	ip nhrp redirect
	ip nhrp shortcut
	ip mtu 1360


route eigrp 123
network 172.16.0.0
network 192.168.44.0
no auto-summary

R5

crypto isakmp policy 10
encr 3des
authentication pre-share
group 2

crypto isakmp key cisco password 0.0.0.0

crypto ipsec transform-set dmtranz esp-3des esp-sh-hmac
	mode transparent

crypto ipsec profile DMVPN
	set transform-set dmtranz

interface tunnel 0
	ip address 172.16.23.5
	tunnel source 7.7.6.5
	tunnel key 123
	tunnel mode gre multipoint
	tunnel protection ipsec profile DMVPN
	ip nhrp network-id 123
	ip nhrp authentication cisco
	ip nhrp map multicast 7.7.8.1
	ip nhrp map multicast 7.7.8.2
	ip nhrp map 172.16.23.1 7.7.8.1
	ip nhrp map 172.16.23.2 7.7.8.2
	ip nhrp nhs 172.16.23.1
	ip nhrp nhs 172.16.23.2
	ip nhrp redirect
	ip nhrp shortcut
	ip mtu 1360


route eigrp 123
network 172.16.0.0
network 192.168.55.0
no auto-summary


asa1

access-list out extended permit udp any any eq isakmp
access-list dmz extended permit udp any any eq isakmp
access-list out extended permit esp any any
access-list dmz extended permit esp any any



~~~~~~~~~~~~

sw6

interface fastethernet 0/2
switchport mode trunk
switchport trunk encapsulation dot1q
no shutdown

interface fastethernet 0/5
switchport mode access
switchport access vlan 7
spanning-tree portfast














































