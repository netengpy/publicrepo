SDWAN v19.2.2
![Topology](https://github.com/netengpy/publicrepo/blob/master/SDWAN/v19-2-2/sdwan-Topology.png)
![Eve-ng](https://github.com/netengpy/publicrepo/blob/master/SDWAN/v19-2-2/sdwan-EveNG-Topology.png)
# Configure OOB, WAN, INTERNET and MPLS
# Config in Underlay_CLI_Configs folder


# VPN ID 0 - Transport VPN (VPN 0)
# VPN ID 512 - Management VPN (VPN 512) for out-of-band management traffic
=======
vManage
=======
```
conf t
vpn 512
interface eth0
ip address 192.168.1.1/24
no shutdown
!
ip route 0.0.0.0/0 192.168.1.254
!
exit
system
host-name vManage
system-ip 1.1.1.1
site-id 1000
organization-name mystacktracecom
vbond 10.1.1.2
!
vpn 0 
int eth1
ip add 10.1.1.1/24
no shut
exit
!
no int eth0
!
ip route 0.0.0.0/0 10.1.1.254
!
commit and-quit
```
********
If it logs commit failed due to:

Aborted: values are not unique: eth0
'vpn 0 interface eth0 if-name'
'vpn 512 interface eth0 if-name'


Delete eth0 on vpn 0 by command:
```
vpn 0
no interface eth0
commit
```
********


======
vBond
======
```
conf t
system
host-name vBond
system-ip 1.1.1.2
site-id 1000
organization-name mystacktracecom
vbond 10.1.1.2 local vbond-only
!
vpn 512 
int eth0
ip add 192.168.1.2/24
no shut
exit
!
ip route 0.0.0.0/0 192.168.1.254
no interface ge0/0
vpn 0 
int ge0/0
no tunnel-interface
ip add 10.1.1.2/24
no shut
exit
!
ip route 0.0.0.0/0 10.1.1.254
!
commit and-quit
```
======
vSmart
======
```
conf t
system
host-name vSmart
system-ip 1.1.1.3
site-id 1000
organization-name mystacktracecom
vbond 10.1.1.2
!
vpn 512 int eth0
ip add 192.168.1.3/24
no shut
exit
!
ip route 0.0.0.0/0 192.168.1.254
!
vpn 0 int eth1
no int eth0
ip add 10.1.1.3/24
no shut
exit
!
ip route 0.0.0.0/0 10.1.1.254
!
commit and-quit
```
=======
Site-300-vEdge01
=======
```
conf t
system
host-name Site-300-vEdge01
system-ip 3.1.1.1
site-id 300
organization-name mystacktracecom
vbond 10.1.1.2
vpn 0 int ge0/0
ip add 200.200.100.18/30
no shutdown
exit
!
ip route 0.0.0.0/0 200.200.100.17
!
commit and-quit
```
=======
Site-400-vEdge02
=======
```
conf t
system
host-name Site-400-vEdge02
system-ip 4.1.1.1
site-id 400
organization-name mystacktracecom
vbond 10.1.1.2
vpn 0 int ge0/0
ip add 200.200.100.14/30
no shutdown
exit
!
ip route 0.0.0.0/0 200.200.100.13
!
commit and-quit
```

========= INSTALL CERTIFICATES =========
openssl rand -out /home/eve/.rnd -hex 256


A CSR Certificate Signing Request file is a file created as a signing request for a digital certificate. It contains an
encrypted block of text that identifies the applicant of the certificate and includes encrypted data for country, state,
organization, domain, email address, and public key.
*.CER or *.CRT - Base64-encoded or DER-encoded binary X.509 Certificate
Storage of a single certificate. This format does not support storage of private keys.

1. root-ca.key on vmanage
2. root-ca.crt from root-ca.key
3. Install .crt on vmanage
4. Generate vmanage_csr on vmanage
5. Create vmanage_crt from vmanage_csr
6. Cat vmanage_crt and Install Certificate on vManage

+ Generate RSA root-ca.key
```
vmanage# vshell
vmanage:~$ openssl genrsa -out root-ca.key 2048
```

+ Create root-ca.crt with root-ca.key
IMPORTANT: Organisation MUST match the Smart Account Organisation
```
vmanage:~$ 
openssl req -x509 -new -nodes -key root-ca.key -sha256 -days 1024 -subj "/C=UK/ST=LON/L=LON/O=mystacktracecom/CN=mystacktracecom/OU=SDWAN-LAB" -out root-ca.crt
```
+ Command to check the created certificate
`openssl x509 -in root-ca.crt -text`

+ Install root-ca.crt
```
exit
vmanage# request root-cert-chain install /home/admin/root-ca.crt
```

`show certificate root-ca-cert`

===========
vManage GUI
===========
Configuration → Certificates → Controllers → vManage → Click on 3 bars → Generate CSR

====================
Go to vManage vshell
====================
```
vmanage# vshell
vmanage:~$ openssl x509 -req -in vmanage_csr -CA root-ca.crt -CAkey root-ca.key -CAcreateserial -out vmanage_crt -days 500 -sha256
```
+ Copy content vmanage.crt file by using “cat vmanage_crt” then install certificate on vManage
`cat vmanage_crt`
Configuration → Certificates → Controllers → Install Certificate → Paste vmanage_crt


From the vManage page (https://19.168.1.1), navigate to Configuration → Devices and then select Controllers. 
Click Add Controller and select vBond from the list. Enter vBond VPN0 IP address, username and password (admin/admin). 
Deselect Generate CSR option and click Add. Repeat the process for the vSmart Controller.

***********
Check on Administration → Settings page. Enter values for Organization Name and vBond IP address. 
Change Controller Certificate Authorization to Enterprise Root certificate and import root-ca.crt
***********

Navigate to Configuration > Certificates and then select Controllers in top left. In the right side for each device press on the three dots button to access Generate CSR option. Copy and paste the content in new file for each node, save files in /root directory as vManage, vBond_csr and vSmart_csr.


======
vBond
======
1. Install root-ca.crt from vManage that was created earlier
2. Add vBond to vManage
3. scp vbond_csr
4. Create vbond_crt from vbond_csr
5. Cat .crt and Install Certificate on vManage
6. Send to vBond

`vBond# request root-cert-chain install scp://admin@192.168.1.1:/home/admin/root-ca.crt vpn 512`

IF FAILS - 
copy/paste root-ca.crt from vmanage and install

show certificate root-ca-cert

+ Add vBond to vManage
```
Configuration → Certificates → Controllers → Add Controller
vBond Mgmt IP: 10.1.1.2
Username: admin
Password: admin
Generate CSR: Check
```
If vbond adding unsuccessful, lets no tunnel-interface as below:
```
vBond# conf t
Entering configuration mode terminal
vBond(config)# vpn 0
vBond(config-vpn-0)# interface ge0/0
vBond(config-interface-ge0/0)# no tunnel-interface
vBond(config-interface-ge0/0)# commit
Commit complete.
vBond(config-interface-ge0/0)#
```

====================
Go to vManage vshell
====================
```
vshell
vmanage:~$ scp admin@10.1.1.2:/home/admin/vbond_csr .
vmanage:~$ openssl x509 -req -in vbond_csr -CA root-ca.crt -CAkey root-ca.key -CAcreateserial -out vbond_crt -days 500 -sha256
```
+ Copy content vbond_crt file by using "cat vbond_crt" then install certificate on vManage
`cat vmanage_crt`
Configuration → Certificates → Controllers → Install Certificate → Paste vbond_crt

+ Send certificate to vBond
Configuration → Certificates → Controllers → Send to vBond

======
vSmart
======
1. Install root-ca.crt from vManage that was created earlier
2. Add vSmart to vManage
3. scp vsmart_csr
4. Create vsmart_crt from vsmart_csr
5. Cat vsmart_crt and Install Certificate on vManage
6. Send to vBond

`vsmart# request root-cert-chain install scp://admin@192.168.1.1:/home/admin/root-ca.crt vpn 512`

IF FAILS - 
copy/paste root-ca.crt from vmanage and install
```
Configuration → Devices → Controllers → Add Controller → vSmart
vSmart Mgmt IP: 10.1.1.3
Username: admin
Password: admin
Protocol: DTLS
Generate CSR: Check
```
====================
Go to vManage vshell
====================
```
vmanage:~$ scp admin@10.1.1.3:/home/admin/vsmart_csr .
vmanage:~$ openssl x509 -req -in vsmart_csr -CA root-ca.crt -CAkey root-ca.key -CAcreateserial -out vsmart_crt -days 500 -sha256
cat vsmart_crt
```
Configuration → Certificates → Controllers → Install Certificate → Paste vsmart_crt

+ Send certificate to vBond
Configuration → Certificates → Controllers → Send to vBond


================================================
Get device list from Cisco using the Smart Account
Upload device list to vManage
================================================
Configuration → Devices → vEdge List → Upload vEdge

+ Validate vEdges
Configuration → Certificates → vEdge List → (vEdge) → Valid

+ Send vedge list to controller
Configuration → Certificates → vEdge List → Send to Controllers

======
vEdge
======
1. Copy and Install root-ca.crt from vManage that was created earlier
2. Activate using chassis and token from vmanage

+ On vManage using “cat root-ca.crt” to see contents then create root-ca.crt file on
vEdge with same contents.
```
vshell
vi root-ca.crt
paste root-ca.crt from vManage
```
+ Install root-ca.crt on vEdge with command:
`vedge# request root-cert-chain install /home/admin/root-ca.crt`

`vedge# request vedge-cloud activate chassis <UUID> token <OTP>`

show certificate root-ca-cert
show control local-properties

========================
Final Task - Config tunnel
Go to vManage and vSmart
========================
```
vpn 0
interface eth1
tunnel-interface
```
======
vBond
======
```
vpn 0
interface ge0/0
tunnel-interface encapsulation ipsec
```

========================
show certificate root-ca-cert
show control connections
show control connections-history
show control local-properties


