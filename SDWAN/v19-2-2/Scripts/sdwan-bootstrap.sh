#!/bin/bash

mkdir certs && cd certs
echo 

printf "\e[1;33m-[INFO]- Generated RSA root-ca.key \e[0m\n"
openssl rand -out /home/eve/.rnd -hex 256
openssl genrsa -out root-ca.key 2048
echo
printf "\e[1;33m-[INFO]- Generating root-ca.crt with root-ca.key \e[0m\n"
echo
printf "\e[1;31mIMPORTANT: Organization MUST match the Cisco Smart Account Organization\e[0m\n"
echo
echo "Example: openssl req -x509 -new -nodes -key root-ca.key -sha256 -days 1024 -subj "/C=UK/ST=LON/L=LON/O=mystacktracecom/CN=mystacktracecom/OU=SDWAN-LAB" -out root-ca.crt"
echo
echo "C=UK ST=LON L=LON O=mystacktracecom OU=SDWAN-LAB CN=mystacktracecom"
echo
openssl req -x509 -new -nodes -key root-ca.key -sha256 -days 1024 -out root-ca.crt
echo
echo "Root Certificate generated."
echo "Press Enter key to continue or crtl+c to exit ..."
read
echo
printf "\e[1;33m-[INFO]- Created Root Certificate \e[0m\n"
openssl x509 -in root-ca.crt -text
echo

printf "\e[1;33m-[INFO]- SCP Root Cert to vBond and vSmart \e[0m\n"
scp root-ca.crt admin@192.168.1.2:/home/admin/
scp root-ca.crt admin@192.168.1.3:/home/admin/
echo
printf "\e[1;33mEnter below command on vBond to install Root Cert. \e[0m\n"
echo "request root-cert-chain install /home/admin/root-ca.crt"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read

printf "\e[1;33mEnter below command vSmart to install Root Cert. \e[0m\n"
echo "request root-cert-chain install /home/admin/root-ca.crt"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read 

printf "\e[1;33m********************************************************
Go to vManage - Administration → Settings
Enter values for Organization Name and vBond IP address
Change Controller Certificate Authorization to Enterprise Root certificate
and Import and Save the root-ca.crt. root-ca.crt was printed above.
********************************************************\e[0m\n"
printf "\e[1;31mIMPORTANT: Organization MUST match the Cisco Smart Account Organization\e[0m\n"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read
printf "\e[1;33mAdd vBond to vManage
Configuration → Devices → Controllers → Add Controller
vBond Mgmt IP: 10.1.1.2
Username: admin
Password: admin
Generate CSR: Check\e[0m\n"
echo
printf "\e[1;33mAdd vSmart to vManage
Configuration → Devices → Controllers → Add Controller
vSmart Mgmt IP: 10.1.1.3
Username: admin
Password: admin
Generate CSR: Check\e[0m\n"

echo 
echo "Press Enter key to continue or crtl+c to exit ..."
read
printf "\e[1;33mGenerate vManage CSR
Configuration → Certificates → Controllers → Generate CSR and close
(Click on the 3 dots in vManage row)\e[0m\n"
echo 
echo "Press Enter key to continue or crtl+c to exit ..."
read
echo 
printf "\e[1;33m-[INFO]- SCP CSRs from vManage, vBond and vSmart\e[0m\n"
echo
scp admin@192.168.1.1:/home/admin/vmanage_csr .
scp admin@192.168.1.2:/home/admin/vbond_csr .
scp admin@192.168.1.3:/home/admin/vsmart_csr .
echo
ls -al | grep _csr
echo 
printf "\e[1;31mMUST see *_csr if not then follow the manaul process to copy the certs\e[0m\n"
echo "Press Enter key to continue or crtl+c to exit ..."
read
echo 
printf "\e[1;33m-[INFO]- Generating Certs for vManage, vBond and vSmart\e[0m\n"
echo
openssl x509 -req -in vmanage_csr -CA root-ca.crt -CAkey root-ca.key -CAcreateserial -out vmanage_crt -days 1024 -sha256
openssl x509 -req -in vbond_csr -CA root-ca.crt -CAkey root-ca.key -CAcreateserial -out vbond_crt -days 1024 -sha256
openssl x509 -req -in vsmart_csr -CA root-ca.crt -CAkey root-ca.key -CAcreateserial -out vsmart_crt -days 1024 -sha256
echo
ls -al | grep _crt
echo
printf "\e[1;31mMUST see *_crt if not then follow the manaul process to generate the certs\e[0m\n"
echo "Press Enter key to continue or crtl+c to exit ..."
read

echo
cat vmanage_crt
echo
printf "\e[1;33mCopy the vManage Cert above and Install on vManage\e[0m\n"
echo "Configuration → Certificates → Controllers → Install Certificate → Paste vmanage_crt"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read
cat vbond_crt
echo
printf "\e[1;33mCopy the vBond Cert above and Install on vManage\e[0m\n"
echo "Configuration → Certificates → Controllers → Install Certificate → Paste vbond_crt"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read
cat vsmart_crt
echo
printf "\e[1;33mCopy the vSmart Cert above and Install on vManage\e[0m\n"
echo "Configuration → Certificates → Controllers → Install Certificate → Paste vsmart_crt"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read

printf "\e[1;33m
========================
Config tunnel
Go to vManage and vSmart
========================
conf t
vpn 0
interface eth1
tunnel-interface
commit and-quit

======
vBond
======
conf t
vpn 0
interface ge0/0
tunnel-interface encapsulation ipsec
commit and-quit
\e[0m\n"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read

printf "\e[1;33m
=================================================
1. Get device list from Cisco using the Smart Account
2. Upload device list to vManage
=================================================
Configuration → Devices → Upload WAN Edge List → Upload serialFile.viptela

+ Validate vEdges
Configuration → Certificates → Valid (Scroll to the right)
+ Send vedge list to controller
Configuration → Certificates → vEdge List → Send to Controllers
\e[0m\n"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read

echo
cat root-ca.crt
echo
printf "\e[1;33mCopy the Root Cert above and Install on vEdges\e[0m\n"
echo 
printf "\e[1;31mGo to vEdge\e[0m\n"
printf "
vshell
vi root-ca.crt
press i on keyboard before pasting
paste root-ca.crt from vManage
press esc then :wq
exit\n"
echo
printf "\e[1;33mInstall root-ca.crt on vEdge with command\e[0m\n"
echo "request root-cert-chain install /home/admin/root-ca.crt"
echo
printf "\e[1;33mGet the chassis and token from vManage\e[0m\n"
echo "request vedge-cloud activate chassis <UUID> token <OTP>"
echo
echo "Press Enter key to continue or crtl+c to exit ..."
read
echo
echo "All Done!"
echo "Go to vManage Main Dashboard."
echo "Some Helpful Show Commands ..."
printf "\e[1;33m
show certificate root-ca-cert
show control connections
show control connections-history
show control local-properties
\e[0m\n"












